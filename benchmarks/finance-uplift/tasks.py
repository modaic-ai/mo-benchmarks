"""Pinned source definitions and exact question shapes for the first finance pilot."""

from dataclasses import dataclass

from modaic import Choice


SEED = 20261002
BASE_MODEL = "modaic/mo"

MULTIFIN_REVISION = "d44a842791acb83a104440a5662b787537ff980b"
BANKING77_REVISION = "3c6d390c3675a24b84c38d827940e275e11183f7"
FINCALC_REVISION = "498b53ab487ece83d38a2ab95ac601b959d319a0"
CFPB_REVISION = "dc9cf40b2d057a58f9168ce00106eefbed309f75"
GERMAN_CREDIT_REVISION = "65eb22f1b213492e8436012bd6c1f51955acddcb"
GOLD_HEADLINES_REVISION = "d8a188f96866372227e1ef9f6fd6230040d3fe75"
FOMC_REVISION = "6b0283f55f0005a6d38d49f271d795c21fccc1a3"
ESG_TEST_REVISION = "6726cff84d342540a63cf5f09a438ff7cebe8c55"
ESG_TRAIN_REVISION = "3009e332a34e639cdd78e2f98b5bd9cb6e99d0dc"
ESG_TRAIN_SHA256 = "60b5307a61202e191117d5d93f38f47d14e4a0bb1da973b5e57e5fe44852bb08"
TWITTER_TOPIC_REVISION = "acbc8af2a35ccf0916124efcbe9e6cf25f191012"
TWITTER_TOPIC_FILE_SHA256 = {
    "topic_train.csv": "63b9ea8183728dd5ddc6a57289341556509ddc0a8d037616519319a316b54490",
    "topic_valid.csv": "67396d6cd4a21c3755de783f20fb5842f12ae8edb9367eed5d2644dd85ca9243",
}

TWITTER_TOPIC_LABELS = (
    "Analyst Update", "Fed | Central Banks", "Company | Product News",
    "Treasuries | Corporate Debt", "Dividend", "Earnings", "Energy | Oil",
    "Financials", "Currencies", "General News | Opinion",
    "Gold | Metals | Materials", "IPO", "Legal | Regulation",
    "M&A | Investments", "Macro", "Markets", "Politics",
    "Personnel Change", "Stock Commentary", "Stock Movement",
)

TWITTER_TOPIC_CRITERIA = {
    "Analyst Update": "Analyst ratings, recommendations, upgrades, downgrades, or price-target changes.",
    "Fed | Central Banks": "The Federal Reserve or another central bank, its officials, or monetary-policy decisions.",
    "Company | Product News": "A company's operations, products, or announcements outside the more specific categories.",
    "Treasuries | Corporate Debt": "Treasury securities, corporate bonds, yields, credit issuance, or debt markets.",
    "Dividend": "A company's dividend payment, increase, cut, or policy.",
    "Earnings": "Company earnings, financial results, guidance, or an earnings report.",
    "Energy | Oil": "Oil, gas, energy commodities, or energy-sector news.",
    "Financials": "Banks, insurers, or other financial-services companies and their business.",
    "Currencies": "Foreign-exchange markets, exchange rates, or currencies.",
    "General News | Opinion": "Broad news or commentary with no more specific listed topic.",
    "Gold | Metals | Materials": "Gold, other metals, mining, or materials commodities.",
    "IPO": "An initial public offering, new stock listing, or the IPO process.",
    "Legal | Regulation": "A lawsuit, enforcement action, regulation, or legal compliance matter.",
    "M&A | Investments": "A merger, acquisition, takeover, or investment deal.",
    "Macro": "Economy-wide conditions or indicators such as inflation, employment, or GDP.",
    "Markets": "Broad financial-market conditions or movements across multiple assets.",
    "Politics": "Political events, elections, or government actions outside a specific regulation.",
    "Personnel Change": "A leadership appointment, departure, promotion, or other personnel change.",
    "Stock Commentary": "Analysis or opinion about a particular stock outside a specific analyst rating update.",
    "Stock Movement": "A particular stock's price move or trading activity.",
}

ESG_LABELS = (
    "Access to Communications", "Biodiversity & Land Use", "Packaging Material & Waste",
    "Financing Environmental Impact", "Carbon Emissions", "Human Capital Development",
    "Ownership & Control", "Community Relations", "Responsible Investment",
    "Opportunities in Renewable Energy", "Consumer Financial Protection", "Accounting",
    "Business Ethics", "Opportunities in Clean Tech", "Toxic Emissions & Waste",
    "Product Carbon Footprint", "Opportunities in Green Building", "Climate Change Vulnerability",
    "Pay", "Water Stress", "Supply Chain Labor Standards", "Chemical Safety", "Board",
    "Opportunities in Nutrition & Health", "Access to Health Care", "Electronic Waste",
    "Access to Finance", "Raw Material Sourcing", "Health & Demographic Risk",
    "Labor Management", "Controversial Sourcing", "Privacy & Data Security",
    "Product Safety & Quality",
)

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
    "twitter-financial-news-topic": Task(
        slug="twitter-financial-news-topic", repo="zeroshot/twitter-financial-news-topic",
        revision=TWITTER_TOPIC_REVISION,
        train_file="topic_train.csv", eval_file="topic_valid.csv",
        eval_split="validation", question_id="topic",
        instructions="Classify the primary topic of this finance-related post. Choose the most specific applicable category.",
        criteria=TWITTER_TOPIC_CRITERIA,
    ),
    "esg": Task(
        slug="esg", repo="ChanceFocus/flare-mlesg", revision=ESG_TEST_REVISION,
        train_file="FinESG-2023_Train_EN.json",
        eval_file="data/test-00000-of-00001-be37870ba5fdb8e5.parquet",
        eval_split="test", question_id="esg_issue",
        instructions="Identify the single most relevant MSCI-style ESG issue in this article.",
        criteria={label: f"The article's most relevant ESG issue is {label}." for label in ESG_LABELS},
    ),
    "german-credit": Task(
        slug="german-credit", repo="ChanceFocus/flare-german", revision=GERMAN_CREDIT_REVISION,
        train_file="data/train-00000-of-00001-fd22df3d350f6dbb.parquet",
        eval_file="data/test-00000-of-00001-3c24c3e9154bed6a.parquet",
        eval_split="test", question_id="creditworthiness",
        instructions="Assess the customer's credit risk from the supplied feature codebook and record.",
        criteria={
            "good": "The customer is classified as good credit risk.",
            "bad": "The customer is classified as bad credit risk.",
        },
    ),
    "gold-headlines": Task(
        slug="gold-headlines", repo="ChanceFocus/flare-headlines", revision=GOLD_HEADLINES_REVISION,
        train_file="data/train-00000-of-00001-b4185af3fde5de2a.parquet",
        eval_file="data/test-00000-of-00001-2a1cddfd1b6bd5cb.parquet",
        eval_split="test", question_id="gold_price",
        instructions="Does this news headline indicate a price or price movement for gold?",
        criteria={
            "Yes": "It indicates a price or price movement for gold.",
            "No": "It does not indicate a price or price movement for gold.",
        },
    ),
    "fomc": Task(
        slug="fomc", repo="gtfintechlab/fomc_communication", revision=FOMC_REVISION,
        train_file="train.csv", eval_file="test.csv", eval_split="test",
        question_id="stance",
        instructions="Classify the monetary-policy stance expressed in this FOMC communication.",
        criteria={
            "dovish": "Supports easier or more accommodative monetary policy.",
            "hawkish": "Supports tighter or more restrictive monetary policy.",
            "neutral": "Expresses neither stance, both stances, or no policy stance.",
        },
    ),
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
