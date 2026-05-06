class V0Agent:
    """No memory, deterministic baseline."""

    def ask(self, message: str) -> str:
        text = message.lower()
        if "return" in text:
            return "I can explain return policy, but I do not keep session context yet."
        if "delivery" in text:
            return "I can explain delivery policy, but I do not keep session context yet."
        return "RetailOps v0: basic response only."
