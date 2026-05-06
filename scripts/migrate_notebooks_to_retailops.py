from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_INPUT = Path(r"C:\ds\ШАД\Pr1\Input")
TARGET_NOTEBOOKS = ROOT / "notebooks"


REPLACEMENTS = {
    # Keep function and variable replacements first for consistency.
    "book_flight": "create_order",
    "search_flights": "search_products",
    "get_booking": "get_order",
    "cancel_booking": "cancel_order",
    "FLIGHTS": "PRODUCTS",
    "flight_id": "product_id",
    "booking_id": "order_id",
    "passenger_profile": "customer_profile",
    "update_passenger_profile": "update_customer_profile",
    # Domain text replacements.
    "flight booking assistant": "retail support assistant",
    "flight booking": "order workflow",
    "airline": "retail",
    "Airline": "Retail",
    "flights": "products",
    "Flights": "Products",
    "flight": "product",
    "Flight": "Product",
    "booking": "order",
    "Booking": "Order",
    "passenger": "customer",
    "Passenger": "Customer",
    "baggage": "delivery",
}


OUTPUT_NAME_MAP = {
    "Agents Week 2026 _ Лекция 1.1 Intro to AI Agents LLM(часть 1).ipynb": "01_llm_basics.ipynb",
    "Agents Week 2026 _ Лекция 1.1 Intro to AI Agents LLM (часть 2).ipynb": "02_first_agent_intro.ipynb",
    "Agents Week 2026 _ Лекция 1.2 Tools. MCP.ipynb": "03_tools_and_mcp.ipynb",
    "Agents Week 2026 _ Семинар 2 Memory and Guardrails in LLM-Powered Agents.ipynb": "04_memory_rag_guardrails.ipynb",
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
                    '    DOMAIN_DIR = Path("data/tau2/domains/retail")'
                ),
            )

        cell["source"] = source.splitlines(keepends=True)

        # Keep notebooks clean and git-stable: strip runtime artifacts.
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def main() -> None:
    TARGET_NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    notebooks = sorted(SOURCE_INPUT.rglob("*.ipynb"))
    if not notebooks:
        raise RuntimeError(f"No notebooks found in {SOURCE_INPUT}")

    for nb in notebooks:
        out_name = OUTPUT_NAME_MAP.get(nb.name, nb.name)
        out_path = TARGET_NOTEBOOKS / out_name
        migrate_notebook(nb, out_path)
        print(f"Migrated: {nb.name} -> {out_path}")


if __name__ == "__main__":
    main()
