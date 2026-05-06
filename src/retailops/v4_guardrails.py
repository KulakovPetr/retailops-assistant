import re

from .v3_rag import V3RagAgent


class V4GuardrailsAgent:
    """RAG + simple safety filters."""

    banned = ("hack", "ignore previous instructions", "exploit")

    @staticmethod
    def mask_pii(text: str) -> str:
        # Mask emails first, then long numeric sequences
        # (used here as a naive card/order identifier proxy).
        masked = re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", "[EMAIL]", text)
        masked = re.sub(r"\b\d{10,16}\b", "[NUMBER]", masked)
        return masked

    def __init__(self) -> None:
        self.rag = V3RagAgent()

    def ask(self, message: str) -> str:
        low = message.lower()
        # Block risky/abusive intents before retrieval.
        if any(token in low for token in self.banned):
            return "Request blocked by guardrails."

        # Sanitize both input and output so examples demonstrate
        # end-to-end privacy handling, not only pre-processing.
        safe_input = self.mask_pii(message)
        answer = self.rag.ask(safe_input)
        return self.mask_pii(answer)
