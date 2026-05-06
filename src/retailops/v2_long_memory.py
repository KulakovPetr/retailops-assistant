class V2LongMemoryAgent:
    """Profile memory across sessions via injected store."""

    def __init__(self, profile_store: dict[str, str] | None = None) -> None:
        self.profile_store = profile_store if profile_store is not None else {}

    def ask(self, message: str) -> str:
        text = message.lower()
        # Write path: persist user name in shared store.
        if text.startswith("my name is "):
            name = message[11:].strip()
            self.profile_store["name"] = name
            return f"Saved name: {name}"
        # Read path: resolve identity from shared store.
        if "who am i" in text:
            if "name" in self.profile_store:
                return f"You are {self.profile_store['name']}"
            return "I do not know your name yet."
        return "Long-term memory active."
