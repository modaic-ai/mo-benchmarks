"""Run resumable, label-blind Gong buying-signal evaluations."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from contextlib import ExitStack
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import httpx
from dotenv import load_dotenv
from modaic import Modaic
from modaic.errors import ModaicAPIError, ModaicConnectionError, ModaicTimeoutError

from questions import DATASET_ID, QUESTION_ID, TASKS, instructions, question
from report import build_report, load_predictions, manifest_hash, read_jsonl


DECISIONS_URL = "https://openrouter.ai/api/alpha/decisions"
CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"
TIMING_METHOD = "successful_attempt_client_http_ms_excludes_retries_v1"


@dataclass(frozen=True)
class ModelSpec:
    name: str
    model: str
    backend: Literal["modaic", "openrouter_decisions", "openrouter_chat"]
    provider: dict[str, Any] | None = None


MODELS = {
    "mo-fast": ModelSpec("mo-fast", "modaic/mo-fast", "modaic"),
    "mo": ModelSpec("mo", "modaic/mo", "modaic"),
    "jev-latest": ModelSpec("jev-latest", "~typesafe/jev-latest", "openrouter_decisions"),
    "luna-decisions": ModelSpec("luna-decisions", "openai/gpt-6-luna-decisions", "openrouter_decisions"),
    "perplexity-decider": ModelSpec("perplexity-decider", "perplexity/pplx-decider-v1.1-27b", "openrouter_decisions"),
    "clef": ModelSpec("clef", "cloudflare/clef", "openrouter_decisions", {"only": ["primeintellect"], "allow_fallbacks": False}),
    "openai-latest": ModelSpec("openai-latest", "openai/gpt-6.1-sol", "openrouter_chat"),
}


def probability(value: Any, item_id: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError(f"{item_id}: model did not return a finite probability")
    return float(value)


def request_state(row: dict[str, Any]) -> dict[str, str]:
    # The model sees only the excerpt; labels never enter this request path.
    return {"conversation_excerpt": row["text"]}


def post_json(client: httpx.Client, url: str, body: dict[str, Any]) -> tuple[dict[str, Any], float]:
    for attempt in range(4):
        started = time.perf_counter()
        try:
            response = client.post(url, json=body)
        except httpx.TransportError:
            if attempt == 3:
                raise
            time.sleep(2**attempt)
            continue
        latency_ms = (time.perf_counter() - started) * 1000
        if response.status_code in (429, 502, 503, 504) and attempt < 3:
            time.sleep(2**attempt)
            continue
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("OpenRouter returned a non-object response")
        return payload, latency_ms
    raise AssertionError("Unreachable retry state")


def chat_body(spec: ModelSpec, row: dict[str, Any]) -> dict[str, Any]:
    return {
        "model": spec.model,
        "messages": [
            {"role": "system", "content": instructions(row["task"]) + " Return only JSON with p_signal, a number between 0 and 1."},
            {"role": "user", "content": json.dumps(request_state(row), ensure_ascii=False)},
        ],
        "response_format": {"type": "json_schema", "json_schema": {
            "name": "buying_signal_probability", "strict": True,
            "schema": {"type": "object", "properties": {"p_signal": {"type": "number"}},
                       "required": ["p_signal"], "additionalProperties": False},
        }},
        "provider": {"require_parameters": True},
        "reasoning": {"effort": "medium"},
        "max_completion_tokens": 1024,
    }


def prediction(row: dict[str, Any], value: Any, latency_ms: float, response: dict[str, Any] | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"id": row["id"], "p_signal": probability(value, row["id"]), "latency_ms": latency_ms}
    if response:
        for key in ("model", "provider"):
            if isinstance(response.get(key), str):
                result["served_model" if key == "model" else key] = response[key]
        cost = response.get("usage", {}).get("cost") if isinstance(response.get("usage"), dict) else None
        if isinstance(cost, (int, float)) and not isinstance(cost, bool) and math.isfinite(cost) and cost >= 0:
            result["cost_usd"] = float(cost)
    return result


def score_row(spec: ModelSpec, row: dict[str, Any], run_hash: str, modaic: Modaic | None, router: httpx.Client | None) -> dict[str, Any]:
    if row["task"] not in TASKS:
        raise ValueError(f"Unknown task: {row['task']}")
    if spec.backend == "modaic":
        assert modaic is not None
        for attempt in range(4):
            started = time.perf_counter()
            try:
                result = modaic.decisions.create(
                    model=spec.model, state=request_state(row), questions={QUESTION_ID: question(row["task"])},
                    capture=False, idempotency_key=f"gong-buying-signals-{run_hash[:16]}-{row['id']}",
                )
            except ModaicAPIError as exc:
                if exc.status_code not in (429, 502, 503, 504) or attempt == 3:
                    raise
            except (ModaicConnectionError, ModaicTimeoutError):
                if attempt == 3:
                    raise
            else:
                answer = result.answers.get(QUESTION_ID)
                return prediction(row, getattr(answer, "noul", None), (time.perf_counter() - started) * 1000,
                                  {"model": spec.model})
            time.sleep(2**attempt)
        raise AssertionError("Unreachable retry state")
    assert router is not None
    if spec.backend == "openrouter_decisions":
        noul = question(row["task"])
        body: dict[str, Any] = {
            "model": spec.model, "state": request_state(row),
            "questions": {QUESTION_ID: {"type": noul.type, **noul.model_dump(exclude_unset=True)}},
        }
        if spec.provider:
            body["provider"] = spec.provider
        result, latency_ms = post_json(router, DECISIONS_URL, body)
        answer = result.get("answers", {}).get(QUESTION_ID)
        if not isinstance(answer, dict) or answer.get("type") != "noul":
            raise ValueError(f"{row['id']}: no Noul answer")
        if spec.name == "clef":
            served = "".join(c for c in str(result.get("provider", "")).lower() if c.isalnum())
            if served != "primeintellect":
                raise ValueError(f"{row['id']}: unexpected Clef provider {result.get('provider')!r}")
        return prediction(row, answer.get("noul"), latency_ms, result)
    body = chat_body(spec, row)
    for attempt in range(4):
        result, latency_ms = post_json(router, CHAT_URL, body)
        choices = result.get("choices")
        if not isinstance(choices, list) or not choices:
            raise ValueError(f"{row['id']}: no chat choice")
        content = choices[0].get("message", {}).get("content")
        try:
            answer = json.loads(content)
        except (TypeError, json.JSONDecodeError):
            if attempt == 3:
                raise ValueError(f"{row['id']}: invalid chat JSON after four attempts") from None
            continue
        if not isinstance(answer, dict) or set(answer) != {"p_signal"}:
            raise ValueError(f"{row['id']}: chat answer must contain only p_signal")
        return prediction(row, answer["p_signal"], latency_ms, result)
    raise AssertionError("Unreachable chat retry state")


def run_model(spec: ModelSpec, data_dir: Path, output_dir: Path, manifest: dict[str, Any],
              limit: int | None, modaic: Modaic | None, router: httpx.Client | None,
              workers: int = 1) -> tuple[int, int]:
    split = "test"
    if workers < 1 or (workers > 1 and spec.backend == "modaic"):
        raise ValueError("Parallel workers require an OpenRouter model")
    config = {
        "name": spec.name, "model": spec.model, "backend": spec.backend, "provider_preferences": spec.provider,
        "dataset_revision": manifest["revision"], "dataset_manifest_sha256": manifest_hash(manifest),
        "split": split, "questions": {task: question(task).model_dump() for task in TASKS},
        "question_id": QUESTION_ID, "threshold": 0.5, "timing_method": TIMING_METHOD,
    }
    if workers != 1:
        config["workers"] = workers
    run_hash = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{spec.name}-{split}.jsonl"
    metadata = output.with_suffix(output.suffix + ".run.json")
    if metadata.exists():
        if json.loads(metadata.read_text(encoding="utf-8")) != config:
            raise ValueError(f"{spec.name}: existing predictions belong to a different run")
    elif output.exists():
        raise ValueError(f"{spec.name}: predictions lack run metadata")
    else:
        metadata.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    completed = load_predictions(output) if output.exists() else {}
    input_bytes = (data_dir / "inputs.jsonl").read_bytes()
    if hashlib.sha256(input_bytes).hexdigest() != manifest["inputs_sha256"]:
        raise ValueError("Input file does not match the benchmark manifest")
    rows = read_jsonl(data_dir / "inputs.jsonl")
    if any(row["split"] != "test" for row in rows):
        raise ValueError("This benchmark permits test inputs only")
    if len(rows) != 200 * len(TASKS) or len({row["id"] for row in rows}) != len(rows):
        raise ValueError("Incomplete or duplicated input cohort")
    if set(completed) - {row["id"] for row in rows}:
        raise ValueError("Existing predictions contain IDs outside the test cohort")
    by_task = {task: [row for row in rows if row["task"] == task and row["id"] not in completed] for task in TASKS}
    remaining = [row for index in range(200) for task in TASKS for row in by_task[task][index:index + 1]]
    if limit is not None:
        remaining = remaining[:limit]
    saved = 0
    with output.open("a", encoding="utf-8") as sink:
        def save(scored: dict[str, Any]) -> None:
            nonlocal saved
            sink.write(json.dumps(scored, ensure_ascii=False) + "\n")
            sink.flush()
            saved += 1
            if saved % 25 == 0:
                print(f"{spec.name}: {saved} new predictions", flush=True)

        if workers == 1:
            for row in remaining:
                save(score_row(spec, row, run_hash, modaic, router))
        else:
            rows_to_run = iter(remaining)
            with ThreadPoolExecutor(max_workers=workers) as pool:
                pending = {}

                def submit_next() -> None:
                    try:
                        row = next(rows_to_run)
                    except StopIteration:
                        return
                    pending[pool.submit(score_row, spec, row, run_hash, modaic, router)] = row["id"]

                for _ in range(workers):
                    submit_next()
                while pending:
                    done, _ = wait(pending, return_when=FIRST_COMPLETED)
                    for future in done:
                        pending.pop(future)
                        try:
                            save(future.result())
                        except Exception:
                            for unfinished in pending:
                                unfinished.cancel()
                            raise
                        submit_next()
    total = len(completed) + saved
    if total == len(rows):
        report = build_report(data_dir, output)
        (output_dir / f"{spec.name}-{split}-report.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    return saved, total


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data/gong"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--models", default="all", help="Comma-separated names or all")
    parser.add_argument("--override", action="append", default=[], metavar="NAME=MODEL_ID")
    parser.add_argument("--timeout", type=float, default=90.0)
    parser.add_argument("--workers", type=int, default=1, help="Concurrent requests for one OpenRouter model (default: 1)")
    parser.add_argument("--external-data-authorized", action="store_true", help="Confirm Gong's written consent covers these model API calls")
    size = parser.add_mutually_exclusive_group(required=True)
    size.add_argument("--limit", type=int, help="At most N new rows per model")
    size.add_argument("--all", action="store_true")
    size.add_argument("--plan", action="store_true")
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1 or args.timeout <= 0 or args.workers < 1:
        parser.error("--limit, --timeout, and --workers must be positive")
    names = list(MODELS) if args.models == "all" else [name.strip() for name in args.models.split(",")]
    if not names or len(set(names)) != len(names) or any(name not in MODELS for name in names):
        parser.error(f"--models must contain distinct names from {', '.join(MODELS)}")
    specs = {name: MODELS[name] for name in names}
    if args.workers > 1 and any(spec.backend == "modaic" for spec in specs.values()):
        parser.error("--workers > 1 is supported only for OpenRouter models")
    for override in args.override:
        name, separator, model = override.partition("=")
        if not separator or name not in specs or not model:
            parser.error("--override must be NAME=MODEL_ID for a selected model")
        previous = specs[name]
        specs[name] = ModelSpec(name, model, previous.backend, previous.provider if model == previous.model else None)
    manifest = json.loads((args.data_dir / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("source") != DATASET_ID:
        parser.error("Not a Gong Call Playbook build")
    if args.plan:
        print(json.dumps({"counts": manifest["counts"], "models": [specs[name].__dict__ for name in names]}, indent=2))
        return
    if not args.external_data_authorized:
        parser.error("Gong's license requires written consent before sending excerpts to third-party model APIs; pass --external-data-authorized only when covered")
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    needs_modaic = any(spec.backend == "modaic" for spec in specs.values())
    needs_router = any(spec.backend != "modaic" for spec in specs.values())
    router_key = os.getenv("OPENROUTER_API_KEY")
    if needs_modaic and not os.getenv("MODAIC_API_KEY"):
        parser.error("Set MODAIC_API_KEY")
    if needs_router and not router_key:
        parser.error("Set OPENROUTER_API_KEY")
    with ExitStack() as stack:
        modaic = stack.enter_context(Modaic(timeout=args.timeout)) if needs_modaic else None
        router = stack.enter_context(httpx.Client(timeout=args.timeout, headers={"Authorization": f"Bearer {router_key}"})) if needs_router else None
        for name in names:
            new, total = run_model(specs[name], args.data_dir, args.output_dir, manifest, args.limit, modaic, router, args.workers)
            print(f"{name}: {new} new, {total}/{200 * len(TASKS)} total", flush=True)


if __name__ == "__main__":
    main()
