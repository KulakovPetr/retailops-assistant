# RetailOps Assistant (Course Working Project)

A minimal, tested project scaffold for the rebuilt agent course.

## Stages
- `v0_no_memory`: basic assistant, tool-like deterministic responses.
- `v1_short_memory`: keeps session context.
- `v2_long_memory`: persists user profile across sessions.
- `v3_rag`: retrieves answers from a small policy knowledge base.
- `v4_guardrails`: adds input/output safety checks and PII masking.

## Run tests
```bash
pip install -r requirements.txt
pytest -q
```

## Why retail
Retail is one of the most active domains for customer-facing AI assistants and has clear, reusable scenarios (returns, delivery, discounts, loyalty, product queries).
