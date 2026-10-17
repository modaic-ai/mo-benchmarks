"""Add audited, taxonomy-grounded rationales to Banking77's captured examples.

The source dataset has intent labels but no human rationales. These are
curated rules applied to the original training utterances, not source-provided
explanations. Ambiguous or contradictory source rows receive no rationale.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from pathlib import Path

from modaic import Modaic, ModaicTimeoutError

from run import DATA, OUTPUTS, TERMINAL, evaluate, get_or_create, read_json, read_jsonl, save_json, score
from tasks import BANKING77_LABELS, TASKS

TASK = TASKS["banking77-routing"]
ROOT = Path(__file__).resolve().parent

# Interpret the actual customer request and draw the closest important boundary.
# These are class-level rules; each annotation also quotes its own source row.
RULES = {
    "Refund_not_showing_up": "A refund is already expected but has not appeared; this differs from asking to initiate a refund.",
    "activate_my_card": "The customer wants to activate or reactivate a card, rather than order or replace one.",
    "age_limit": "The question is about eligibility by age, including whether a child can hold an account.",
    "apple_pay_or_google_pay": "The request concerns using a card or top-up through Apple Pay, Google Pay, or a linked watch; the wallet channel is the specific subject.",
    "atm_support": "The question is where or which ATMs can be used, rather than whether a particular withdrawal was declined.",
    "automatic_top_up": "The customer asks about automatic or recurring balance replenishment, rather than a one-time top-up.",
    "balance_not_updated_after_bank_transfer": "Money transferred into the customer's account has not appeared in the balance; this concerns account posting rather than the transfer's general timing.",
    "balance_not_updated_after_cheque_or_cash_deposit": "A cheque or cash deposit has not appeared in the customer's account balance; the deposit method distinguishes it from a bank transfer.",
    "beneficiary_not_allowed": "The recipient or beneficiary is being disallowed; this is more specific than an unexplained transfer failure.",
    "cancel_transfer": "The customer wants to stop or undo a transfer they initiated, rather than troubleshoot its delivery.",
    "card_about_to_expire": "An existing card is near expiry and the customer asks about renewal or replacement before expiry.",
    "card_acceptance": "The customer asks where a card can be used or accepted, rather than which countries the banking service operates in.",
    "card_arrival": "The customer asks about the status or non-arrival of a card already ordered, not a general delivery-time estimate.",
    "card_delivery_estimate": "The customer asks how long card delivery normally takes or for a delivery date, rather than reporting a specific missing shipment.",
    "card_linking": "The customer needs to connect or restore access to an existing card in the account; the card is already in their possession.",
    "card_not_working": "The card has a general functionality problem, with no clearly identified transaction type or explicit decline to route more narrowly.",
    "card_payment_fee_charged": "The disputed fee is attached to a card purchase or card payment, not a bank transfer or cash withdrawal.",
    "card_payment_not_recognised": "A posted card payment is unfamiliar to the customer; the issue is recognition, not a payment decline.",
    "card_payment_wrong_exchange_rate": "A card purchase in another currency used an allegedly wrong exchange rate; this is a transaction-specific complaint.",
    "card_swallowed": "An ATM retained the physical card, regardless of whether cash was dispensed.",
    "cash_withdrawal_charge": "The question is a fee for withdrawing cash, not the cash amount or exchange rate.",
    "cash_withdrawal_not_recognised": "The statement shows an ATM withdrawal the customer does not recognize, rather than a failed withdrawal attempt.",
    "change_pin": "The customer asks to set or change a card PIN, not recover an app login passcode.",
    "compromised_card": "The customer suspects unauthorized use or compromise of the card and needs a card-security route.",
    "contactless_not_working": "The contactless payment feature specifically fails, rather than the whole card or a generic purchase.",
    "country_support": "The question is which countries the banking service operates in, rather than where a particular card is accepted.",
    "declined_card_payment": "A card purchase at a merchant was explicitly rejected; distinguish that failed attempt from a pending card payment.",
    "declined_cash_withdrawal": "An attempted ATM cash withdrawal was rejected; distinguish it from a card purchase being declined.",
    "declined_transfer": "A transfer was explicitly declined by the service, rather than merely pending or late to arrive.",
    "direct_debit_payment_not_recognised": "An unfamiliar direct debit or mandate appears; this is a direct-debit issue, not an ordinary card purchase.",
    "disposable_card_limits": "The customer asks about limits or restrictions on disposable virtual cards, not about obtaining one.",
    "edit_personal_details": "The customer wants to change account profile information such as their address or personal data.",
    "exchange_charge": "The request concerns fees for converting currencies, not the exchange rate itself.",
    "exchange_rate": "The request asks what conversion rate applies or how it varies, without disputing a particular completed transaction.",
    "exchange_via_app": "The customer asks how to exchange one currency for another in the app, not whether a currency is supported.",
    "extra_charge_on_statement": "The statement contains an extra amount or unexplained surcharge, without a more specific payment-method fee being established.",
    "failed_transfer": "Repeated transfer attempts fail to complete; this is a transfer execution failure rather than a completed transfer awaiting receipt.",
    "fiat_currency_support": "The customer asks which government-issued currencies can be held or used in the account.",
    "get_disposable_virtual_card": "The customer wants to obtain a disposable virtual card, not learn its spending limits.",
    "get_physical_card": "The customer asks about getting a standard physical card or its initial setup, rather than ordering an additional spare.",
    "getting_spare_card": "The customer wants an additional card beyond the one already held; this differs from a first physical-card order.",
    "getting_virtual_card": "The customer wants to obtain or find an ordinary virtual card, rather than a disposable card.",
    "lost_or_stolen_card": "The physical card has been lost or stolen and the customer needs the card-loss route.",
    "lost_or_stolen_phone": "The phone used for account access has been lost or stolen; the missing object is the phone, not the card.",
    "order_physical_card": "The customer asks how to place an order for a physical card, not where a previously ordered card is.",
    "passcode_forgotten": "The customer cannot recall the app access passcode; this differs from a blocked card PIN.",
    "pending_card_payment": "A card purchase is still marked pending; it has not been explicitly declined or reversed.",
    "pending_cash_withdrawal": "An ATM withdrawal is still pending; the operation is cash withdrawal, not a card purchase.",
    "pending_top_up": "An account top-up is pending or has not finished processing, rather than definitively failed.",
    "pending_transfer": "A bank transfer is explicitly pending, rather than declined, failed, or confirmed missing at the recipient.",
    "pin_blocked": "Too many incorrect card PIN attempts caused a block; this is distinct from simply changing a PIN.",
    "receiving_money": "The customer asks how to receive funds into the account, rather than send a transfer out.",
    "request_refund": "The customer wants to obtain a refund or learn the refund policy, rather than locate a refund already issued.",
    "reverted_card_payment?": "A card purchase was reversed and the money returned; this is a reversal, not a pending or merely declined payment.",
    "supported_cards_and_currencies": "The customer asks which external cards or currencies are accepted for account use or top-up.",
    "terminate_account": "The customer wants to close or delete the account, not merely change its details.",
    "top_up_by_bank_transfer_charge": "The question is a fee for adding money through a bank transfer, not a card top-up or cash deposit.",
    "top_up_by_card_charge": "The customer asks about a fee for topping up with a payment card, not a bank-transfer fee.",
    "top_up_by_cash_or_cheque": "The customer asks how or where to deposit cash or a cheque to add money to the account.",
    "top_up_failed": "An attempted account top-up was rejected or failed, rather than merely remaining pending.",
    "top_up_limits": "The customer asks for minimums, maximums, or restrictions on account top-ups.",
    "top_up_reverted": "A top-up initially appeared or completed and was later reversed or removed.",
    "topping_up_by_card": "The customer asks how to add money with a payment card, rather than about a fee or a failed attempt.",
    "transaction_charged_twice": "The same transaction was charged twice; the duplicate posting is the central issue.",
    "transfer_fee_charged": "The disputed fee is for a bank transfer, not a card purchase or cash withdrawal.",
    "transfer_into_account": "The customer asks how to move money into the account by bank transfer, rather than by card or cash deposit.",
    "transfer_not_received_by_recipient": "A sent transfer has not arrived with its intended recipient; distinguish the recipient's receipt from the sender's account balance.",
    "transfer_timing": "The question is the normal time a transfer takes, not a known decline or a specific missing recipient payment.",
    "unable_to_verify_identity": "The customer has attempted identity verification but cannot complete it, rather than asking why verification is required.",
    "verify_my_identity": "The customer asks how or with what documents to verify their identity, rather than reporting a failed attempt.",
    "verify_source_of_funds": "The customer asks how to prove or verify the origin of their funds, not general identity verification.",
    "verify_top_up": "The customer needs to verify a top-up, often through a missing verification code; this is transaction verification, not identity proof.",
    "virtual_card_not_working": "A virtual card fails to work, rather than a physical card or contactless feature.",
    "visa_or_mastercard": "The customer asks which card network, Visa or Mastercard, is issued or available, not which top-up cards are accepted.",
    "why_verify_identity": "The customer asks why identity checks are necessary, rather than how to perform them.",
    "wrong_amount_of_cash_received": "An ATM dispensed a different cash amount than requested; the issue is quantity, not withdrawal fees or exchange rate.",
    "wrong_exchange_rate_for_cash_withdrawal": "An ATM cash withdrawal used an allegedly wrong currency conversion rate, not a card purchase rate.",
}

# These source labels cannot be justified from the utterance alone. Do not
# invent evidence to make them look well-supported. The label remains as in
# the first alignment; the second pass only adds rationales where defensible.
AMBIGUOUS_ROWS = {
    "train-1215": "says transaction, not transfer",
    "train-138": "does not say activation is needed",
    "train-2163": "mentions a fee but no card payment",
    "train-3799": "mentions a charge but no direct debit",
    "train-5034": "asks about PIN, not getting a card",
    "train-5543": "asks whether the phone is needed, not whether it was lost",
    "train-5897": "does not establish pending rather than failed",
    "train-7416": "mentions cash, not bank transfer",
    "train-8466": "online purchase does not establish a bank-transfer fee",
    "train-8759": "asks about a receipt, not recipient receipt",
    "train-3125": "asks for a new card but does not mention contactless",
    "train-3663": "online payment does not establish a transfer",
    "train-3660": "purchase does not establish a transfer",
    "train-5130": "asks about creating PIN, not getting a card",
    "train-5104": "asks about PIN, not getting a card",
    "train-7065": "merchant rejection does not establish a reversal",
    "train-7374": "SWIFT question does not establish a top-up fee",
    "train-8078": "describes money disappearing after top-up, not how to top up",
    "train-8073": "top up my card does not establish a card-funded top-up",
    "train-1035": "failed transfer does not establish an invalid beneficiary",
    "train-1036": "transfer impossible does not establish an invalid beneficiary",
    "train-2115": "mentions account fees but no specific card payment",
    "train-5785": "passcode not working does not establish that it was forgotten",
    "train-6038": "transaction pending does not establish a cash withdrawal",
    "train-1156": "asks to move payment from an account; cancellation is not explicit",
    "train-6507": "already received salary and asks about configuration",
    "train-9283": "verification code has no top-up context",
    "train-9537": "choice of card does not establish Visa or Mastercard network",
    "train-1891": "Netflix decline does not establish general card failure",
    "train-5635": "delivery-services question does not establish placing a card order",
    "train-5015": "asks how to use disposable cards, not how to obtain one",
    "train-5545": "says phone was lost, but request is about card use; retain label without rationale",
    "train-8782": "payment not posted does not establish recipient-side nonreceipt",
}


def rationale(row: dict) -> str | None:
    if row["id"] in AMBIGUOUS_ROWS:
        return None
    utterance = " ".join(row["state"]["conversation"].split())
    if not utterance:
        return None
    rule = RULES[row["truth"]]
    return f'Customer wording: “{utterance}”\nRouting reason: {rule}'


def verify_rules(cohort: dict) -> None:
    if set(RULES) != set(BANKING77_LABELS):
        raise RuntimeError(f"reasoning rules cover {len(RULES)} of {len(BANKING77_LABELS)} labels")
    if any(r["truth"] not in RULES for r in cohort["train_rows"]):
        raise RuntimeError("unknown truth label")
    if len(cohort["train_rows"]) > 200:
        raise RuntimeError("label cap exceeded")
    if not (150 <= sum(rationale(r) is not None for r in cohort["train_rows"]) <= 200):
        raise RuntimeError("unexpected rationale coverage")


def annotate(model, cohort: dict) -> dict:
    records = read_jsonl(OUTPUTS / f"{TASK.slug}.train.jsonl")
    if len(records) != len(cohort["train_rows"]):
        raise RuntimeError("captured training records incomplete")
    path = OUTPUTS / f"{TASK.slug}.reasoning.jsonl"
    done = read_jsonl(path)
    for row in cohort["train_rows"]:
        text = rationale(row)
        if text is None:
            continue
        digest = hashlib.sha256(text.encode()).hexdigest()
        if done.get(row["id"], {}).get("sha256") == digest:
            continue
        original = records[row["id"]]
        example = model.examples.annotate(original["example_id"], ground_reasoning=text)
        annotation = example.annotation
        if (not annotation or annotation.ground_truth != {TASK.question_id: row["truth"]}
                or annotation.ground_reasoning != text or annotation.split != original["split"]):
            raise RuntimeError(f"annotation did not preserve truth and split: {row['id']}")
        record = {"id": row["id"], "example_id": original["example_id"], "sha256": digest,
                  "ground_reasoning": text, "split": annotation.split}
        with path.open("a") as out:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
        done[row["id"]] = record
        if len(done) % 25 == 0:
            print(f"  {len(done)} rationales annotated", flush=True)
    expected = sum(rationale(r) is not None for r in cohort["train_rows"])
    if len(done) != expected:
        raise RuntimeError(f"only {len(done)} of {expected} rationale updates completed")
    return {"rationales_added": expected, "ambiguous_without_reasoning": len(cohort["train_rows"]) - expected}


def align(client, model, state: dict, path: Path, budget: int) -> dict:
    if not state.get("reasoning_alignment_id"):
        job = model.jobs.alignments.create(
            branch="main", source_commit_sha=state["result_revision"],
            max_metric_calls=budget,
            idempotency_key=f"finance-uplift-reasoning-align-{TASK.slug}-{state['cohort_sha256'][:16]}",
        )
        state["reasoning_alignment_id"] = job.id
        save_json(path, state)
        print(f"reasoning alignment queued: {job.id}", flush=True)
    while True:
        try:
            job = client.alignments.wait(state["reasoning_alignment_id"], timeout=300, poll_interval=10)
        except ModaicTimeoutError:
            print("reasoning alignment still running", flush=True)
            continue
        if job.status in TERMINAL:
            break
    state["reasoning_alignment_status"] = job.status
    state["reasoning_result_revision"] = job.result_commit_sha or state["result_revision"]
    state["reasoning_alignment_result"] = job.result
    save_json(path, state)
    if job.status != "completed":
        raise RuntimeError(f"reasoning alignment {job.status}: {job.error}")
    if not job.result_commit_sha:
        state["reasoning_batch_status"] = "not_applicable"
        save_json(path, state)
        return state
    print(f"reasoning alignment completed at {job.result_commit_sha[:10]}; waiting for batch", flush=True)
    batch_id = state.get("reasoning_batch_id")
    while not batch_id:
        matches = [b for b in model.jobs.batch_decisions.list(limit=20).batch_decisions
                   if b.source_commit_sha == job.result_commit_sha]
        if matches:
            batch_id = matches[0].id
            state["reasoning_batch_id"] = batch_id
            save_json(path, state)
            break
        time.sleep(10)
    while True:
        try:
            batch = client.batch_decisions.wait(batch_id, timeout=300, poll_interval=10)
        except ModaicTimeoutError:
            print("reasoning follow-up batch still running", flush=True)
            continue
        if batch.status in TERMINAL:
            break
    state["reasoning_batch_status"] = batch.status
    state["reasoning_batch_progress"] = batch.progress.model_dump() if batch.progress else None
    save_json(path, state)
    if batch.status != "completed" or (batch.progress and batch.progress.failed):
        raise RuntimeError(f"reasoning follow-up batch {batch.status}: {batch.progress}")
    print("reasoning follow-up batch completed", flush=True)
    return state


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=["preview", "annotate", "align", "final"], required=True)
    parser.add_argument("--workspace", default=os.environ.get("MODAIC_WORKSPACE", "modaic_labs"))
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--max-metric-calls", type=int, default=200)
    args = parser.parse_args()
    cohort = read_json(DATA / f"{TASK.slug}.json")
    verify_rules(cohort)
    if args.phase == "preview":
        for row in cohort["train_rows"]:
            print(json.dumps({"id": row["id"], "truth": row["truth"], "rationale": rationale(row),
                              "omission_reason": AMBIGUOUS_ROWS.get(row["id"])}, ensure_ascii=False))
        return
    if not os.environ.get("MODAIC_API_KEY"):
        parser.error("MODAIC_API_KEY is required")
    path = OUTPUTS / f"{TASK.slug}.state.json"
    state = read_json(path, {})
    if state.get("cohort_sha256") != cohort["sha256"] or state.get("batch_status") != "completed":
        raise RuntimeError("complete the first alignment and follow-up batch first")
    with Modaic(timeout=180) as client:
        model = get_or_create(client, TASK, cohort, args.workspace)
        if model.id != state["model_id"]:
            raise RuntimeError("model identity changed")
        if args.phase == "annotate":
            state.update(annotate(model, cohort))
            save_json(path, state)
        elif args.phase == "align":
            if state.get("rationales_added") != sum(rationale(r) is not None for r in cohort["train_rows"]):
                raise RuntimeError("rationale annotation incomplete")
            align(client, model, state, path, args.max_metric_calls)
        else:
            if state.get("reasoning_alignment_status") != "completed" or state.get("reasoning_batch_status") not in {"completed", "not_applicable"}:
                raise RuntimeError("wait for reasoning alignment and follow-up batch first")
            baseline = read_jsonl(OUTPUTS / f"{TASK.slug}.baseline.jsonl")
            label_only = read_jsonl(OUTPUTS / f"{TASK.slug}.final.jsonl")
            # If alignment publishes no checkpoint, the served model is exactly
            # the first checkpoint. Reuse its decisions instead of turning API
            # sampling noise into a purported effect of reasoning.
            final = (label_only if state["reasoning_result_revision"] == state["result_revision"]
                     else evaluate(model, TASK, cohort, "reasoning-final", state["reasoning_result_revision"], args.workers))
            report = score(TASK, baseline, final, cohort["eval_rows"])
            intermediate = score(TASK, baseline, label_only, cohort["eval_rows"])
            report.update({
                "model_path": state["model_path"], "cohort_sha256": cohort["sha256"],
                "baseline_revision": state["baseline_revision"],
                "label_only_revision": state["result_revision"],
                "aligned_revision": state["reasoning_result_revision"],
                "label_only_accuracy": intermediate["aligned_accuracy"],
                "label_only_uplift_pp": intermediate["uplift_pp"],
                "reasoning_vs_label_only_pp": (report["aligned_accuracy"] - intermediate["aligned_accuracy"]) * 100,
                "alignment_id": state["reasoning_alignment_id"],
                "batch_id": state.get("reasoning_batch_id"),
                "batch_status": state["reasoning_batch_status"],
                "training_labels": len(cohort["train_rows"]),
                "ground_reasoning_count": state["rationales_added"],
                "reasoning_provenance": "curated from training utterances and Banking77 taxonomy; not source-provided",
            })
            save_json(OUTPUTS / f"{TASK.slug}.reasoning.report.json", report)
            print(json.dumps(report, indent=2), flush=True)


if __name__ == "__main__":
    main()
