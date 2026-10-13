"""Pinned source definitions and exact question shapes for the first finance pilot."""

from dataclasses import dataclass

from modaic import Choice


SEED = 20261002
BASE_MODEL = "modaic/mo"

MULTIFIN_REVISION = "d44a842791acb83a104440a5662b787537ff980b"
BANKING77_REVISION = "3c6d390c3675a24b84c38d827940e275e11183f7"
FINCALC_REVISION = "498b53ab487ece83d38a2ab95ac601b959d319a0"
CFPB_REVISION = "dc9cf40b2d057a58f9168ce00106eefbed309f75"

CFPB_SUBISSUES = (
    "Information belongs to someone else",
    "Their investigation did not fix an error on your report",
    "Reporting company used your report improperly",
    "Account status incorrect",
    "Was not notified of investigation status or results",
    "Account information incorrect",
    "Credit inquiries on your report that you don't recognize",
    "Investigation took more than 30 days",
    "Debt is not yours",
    "Debt was result of identity theft",
)

BANKING77_LABELS = (
    "activate_my_card", "age_limit", "apple_pay_or_google_pay", "atm_support",
    "automatic_top_up", "balance_not_updated_after_bank_transfer",
    "balance_not_updated_after_cheque_or_cash_deposit", "beneficiary_not_allowed",
    "cancel_transfer", "card_about_to_expire", "card_acceptance", "card_arrival",
    "card_delivery_estimate", "card_linking", "card_not_working",
    "card_payment_fee_charged", "card_payment_not_recognised",
    "card_payment_wrong_exchange_rate", "card_swallowed", "cash_withdrawal_charge",
    "cash_withdrawal_not_recognised", "change_pin", "compromised_card",
    "contactless_not_working", "country_support", "declined_card_payment",
    "declined_cash_withdrawal", "declined_transfer", "direct_debit_payment_not_recognised",
    "disposable_card_limits", "edit_personal_details", "exchange_charge", "exchange_rate",
    "exchange_via_app", "extra_charge_on_statement", "failed_transfer", "fiat_currency_support",
    "get_disposable_virtual_card", "get_physical_card", "getting_spare_card",
    "getting_virtual_card", "lost_or_stolen_card", "lost_or_stolen_phone",
    "order_physical_card", "passcode_forgotten", "pending_card_payment",
    "pending_cash_withdrawal", "pending_top_up", "pending_transfer", "pin_blocked",
    "receiving_money", "Refund_not_showing_up", "request_refund", "reverted_card_payment?",
    "supported_cards_and_currencies", "terminate_account", "top_up_by_bank_transfer_charge",
    "top_up_by_card_charge", "top_up_by_cash_or_cheque", "top_up_failed", "top_up_limits",
    "top_up_reverted", "topping_up_by_card", "transaction_charged_twice",
    "transfer_fee_charged", "transfer_into_account", "transfer_not_received_by_recipient",
    "transfer_timing", "unable_to_verify_identity", "verify_my_identity", "verify_source_of_funds",
    "verify_top_up", "virtual_card_not_working", "visa_or_mastercard", "why_verify_identity",
    "wrong_amount_of_cash_received", "wrong_exchange_rate_for_cash_withdrawal",
)


@dataclass(frozen=True)
class Task:
    slug: str
    repo: str
    revision: str
    train_file: str
    eval_file: str
    eval_split: str
    question_id: str
    instructions: str
    criteria: dict[str, str]

    @property
    def question(self) -> Choice:
        return Choice(instructions=self.instructions, criteria=self.criteria)


TASKS = {
    "multifin": Task(
        slug="multifin", repo="awinml/MultiFin", revision=MULTIFIN_REVISION,
        train_file="only_english_highlevel/train-00000-of-00001.parquet",
        eval_file="only_english_highlevel/validation-00000-of-00001.parquet",
        eval_split="validation", question_id="topic",
        instructions="Classify the primary topic of this financial-services headline.",
        criteria={
            "Finance": "Finance, funding, investment, or financial markets.",
            "Technology": "Technology, data, or digital transformation.",
            "Tax & Accounting": "Tax, audit, accounting, or financial reporting.",
            "Business & Management": "Business strategy, management, or operations.",
            "Government & Controls": "Government, regulation, controls, or compliance.",
            "Industry": "A sector- or industry-specific subject.",
        },
    ),
    "banking77-routing": Task(
        slug="banking77-routing", repo="DeepPavlov/banking77", revision=BANKING77_REVISION,
        train_file="data/train-00000-of-00001.parquet",
        eval_file="data/test-00000-of-00001.parquet",
        eval_split="test", question_id="banking_intent",
        instructions=(
            "Route the customer's banking-support request to the single most specific Banking77 intent. "
            "Distinguish closely related transaction states such as pending, declined, failed, reverted, fee, and unrecognized."
        ),
        criteria={
            label: "The request concerns: " + label.replace("_", " ").replace("?", "").lower() + "."
            for label in BANKING77_LABELS
        },
    ),
    "fincalc-nli": Task(
        slug="fincalc-nli", repo="anespo28/fincalc-nli", revision=FINCALC_REVISION,
        train_file="train.jsonl", eval_file="test.jsonl", eval_split="test",
        question_id="verdict",
        instructions=(
            "Judge whether the financial claim follows from the supplied evidence. "
            "Check numerical calculations and stated relationships. Use only the evidence: "
            "entailment means it supports the claim, contradiction means it conflicts, "
            "and neutral means it does not settle the claim."
        ),
        criteria={
            "contradiction": "The evidence conflicts with the claim, including an incorrect calculation or threshold conclusion.",
            "entailment": "The evidence establishes the claim, including any required calculation.",
            "neutral": "The evidence does not contain enough information to establish or contradict the claim.",
        },
    ),
    "cfpb-routing": Task(
        slug="cfpb-routing", repo="Johnade/consumer_complaints_cfpb", revision=CFPB_REVISION,
        train_file="train_consumer_complaints.csv", eval_file="test_consumer_complaints.csv",
        eval_split="test", question_id="complaint_issue",
        instructions="Route this consumer financial complaint to its most specific listed issue.",
        criteria={label: f"The complaint is primarily about: {label}." for label in CFPB_SUBISSUES},
    ),
}
