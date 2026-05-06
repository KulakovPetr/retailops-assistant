class V1ShortMemoryAgent:
    """Session memory only."""

    def __init__(self) -> None:
        self.history: list[str] = []

    def ask(self, message: str) -> str:
        self.history.append(message)
        text = message.lower()
        if "what did i ask" in text:
            if len(self.history) < 2:
                return "No previous question in this session."
            return f"Previous question: {self.history[-2]}"
        return "Stored in short-term memory."
