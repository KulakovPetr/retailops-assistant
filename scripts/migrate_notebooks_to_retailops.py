from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_INPUT = Path(r"C:\ds\ШАД\Pr1\Input")
TARGET_NOTEBOOKS = ROOT / "notebooks"


REPLACEMENTS = {
    "airline": "retail",
    "Airline": "Retail",
    "flight booking assistant": "retail support assistant",
    "flight booking": "order workflow",
    "flights": "products",
    "Flights": "Products",
    "flight": "product",
    "Flight": "Product",
    "booking": "order",
    "Booking": "Order",
    "book_flight": "create_order",
    "search_flights": "search_products",
    "get_booking": "get_order",
    "cancel_booking": "cancel_order",
    "passenger": "customer",
    "Passenger": "Customer",
    "baggage": "delivery",
}


RETAIL_POLICIES_CELL = """# Retail policy handbook: 13 concise chunks for RAG demos.
# Written in formal style on purpose to preserve HyDE behavior from the original lesson.
POLICIES = [
    {
        "title": "Return Window",
        "content": (
            "Customers may return eligible products within 14 calendar days from delivery date. "
            "Items must be in resalable condition unless a defect is documented."
        ),
    },
    {
        "title": "Refund Processing",
        "content": (
            "Refunds are issued to the original payment method after return acceptance. "
            "Typical processing time is 3-10 business days depending on payment provider."
        ),
    },
    {
        "title": "Defective Item Exception",
        "content": (
            "Defective products are eligible for full refund or replacement beyond standard return window, "
            "provided defect evidence is submitted and validated."
        ),
    },
    {
        "title": "Opened Electronics Policy",
        "content": (
            "Opened electronics are non-returnable unless hardware defect is confirmed. "
            "Cosmetic wear and buyer remorse are not considered defects."
        ),
    },
    {
        "title": "Delivery Delay Compensation",
        "content": (
            "If delivery exceeds the promised window by more than 48 hours, customer may claim compensation "
            "as store credit according to order value tiers."
        ),
    },
    {
        "title": "Order Cancellation by Customer",
        "content": (
            "Customer may cancel before shipment confirmation with no fee. "
            "After shipment, cancellation is treated as return after delivery."
        ),
    },
    {
        "title": "Order Cancellation by Merchant",
        "content": (
            "If merchant cancels due to stock issues, customer receives full refund and optional promo credit."
        ),
    },
    {
        "title": "Partial Refund Rules",
        "content": (
            "Partial refund may be applied for minor quality issues when customer keeps the product, "
            "subject to support review and approval."
        ),
    },
    {
        "title": "Loyalty Cashback",
        "content": (
            "Loyalty members receive cashback percentage based on tier. "
            "Cashback is credited after order completion and expires by program rules."
        ),
    },
    {
        "title": "Promo Code Eligibility",
        "content": (
            "Promo codes are valid only for eligible categories and minimum basket amount. "
            "Codes cannot be combined unless explicitly stated."
        ),
    },
    {
        "title": "Warranty Claim Intake",
        "content": (
            "Warranty claims require order identifier, issue description, and photo/video evidence. "
            "Support response SLA is up to 2 business days."
        ),
    },
    {
        "title": "Address Change Restrictions",
        "content": (
            "Address changes are allowed before courier handoff. "
            "After handoff, redirection depends on carrier support and region constraints."
        ),
    },
    {
        "title": "Fraud Review Hold",
        "content": (
            "Orders flagged by risk systems may be temporarily placed on hold pending identity or payment verification."
        ),
    },
]

print(f"✅ Loaded {len(POLICIES)} retail policy chunks")
"""


def transform_cell_source(source: str) -> str:
    out = source
    for old, new in REPLACEMENTS.items():
        out = out.replace(old, new)
    return out


def migrate_notebook(src: Path, dst: Path) -> None:
    data = json.loads(src.read_text(encoding="utf-8"))

    for idx, cell in enumerate(data.get("cells", [])):
        source = "".join(cell.get("source", []))
        source = transform_cell_source(source)

        # Seminar notebook: replace policy corpus completely.
        if (
            "Семинар 2 Memory and Guardrails" in str(src)
            and idx == 22
            and "POLICIES" in source
        ):
            source = RETAIL_POLICIES_CELL

        # Part 2 lecture: keep fallback path so notebook remains runnable.
        if "Intro to AI Agents LLM (часть 2)" in src.name and idx == 7:
            source = source.replace(
                'DOMAIN_DIR = Path("data/tau2/domains/retail")',
                (
                    '# Prefer retail domain; fallback keeps notebook runnable.\n'
                    'DOMAIN_DIR = Path("data/tau2/domains/retail")\n'
                    'if not DOMAIN_DIR.exists():\n'
                    '    DOMAIN_DIR = Path("data/tau2/domains/airline")'
                ),
            )

        cell["source"] = source.splitlines(keepends=True)

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def main() -> None:
    TARGET_NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    notebooks = sorted(SOURCE_INPUT.rglob("*.ipynb"))
    if not notebooks:
        raise RuntimeError(f"No notebooks found in {SOURCE_INPUT}")

    for nb in notebooks:
        rel = nb.relative_to(SOURCE_INPUT)
        out_path = TARGET_NOTEBOOKS / rel.name
        migrate_notebook(nb, out_path)
        print(f"Migrated: {nb.name} -> {out_path}")


if __name__ == "__main__":
    main()
