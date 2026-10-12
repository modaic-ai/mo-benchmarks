#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -ne 1 || "$1" != "--external-data-authorized" ]]; then
  echo "Usage: ./reproduce.sh --external-data-authorized" >&2
  echo "Run only after Gong's written consent covers dataset use and calls to both model API providers." >&2
  exit 2
fi

for tool in uv node; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "Missing required command: $tool" >&2
    exit 1
  fi
done

benchmark_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$benchmark_dir/../.." && pwd)"
cd "$benchmark_dir"

uv sync --locked
uv run --locked python prepare.py
uv run --locked python - <<'PY'
import json
from pathlib import Path
from report import manifest_hash

manifest = json.loads(Path("data/gong/manifest.json").read_text(encoding="utf-8"))
published = json.loads(Path("../../data/buying-signals.json").read_text(encoding="utf-8"))
if manifest_hash(manifest) != published["cohort_sha256"]:
    raise SystemExit("Prepared test cohort differs from the published benchmark cohort")
print("Prepared test cohort matches the published benchmark")
PY

uv run --locked python run_models.py --models mo-fast,mo --all --external-data-authorized
uv run --locked python run_models.py --models jev-latest,luna-decisions,perplexity-decider,clef --all --external-data-authorized
uv run --locked python run_models.py --models openai-latest --workers 8 --output-dir outputs/load-8 --all --external-data-authorized
uv run --locked python compare.py --output-dir outputs --output outputs/leaderboard.md

cd "$repo_root"
node scripts/import-buying-signals.mjs
printf 'Complete. Reports: benchmarks/buying-signals/outputs/\nSite aggregates: data/buying-signals.json\n'
