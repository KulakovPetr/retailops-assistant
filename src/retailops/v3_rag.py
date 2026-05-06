from .data import POLICIES


class V3RagAgent:
    """Tiny keyword retrieval over policy docs.

    Educational intent:
    - keep retrieval logic explicit and readable;
    - show scoring without hidden framework magic;
    - provide a baseline before adding guardrails.
    """

    def ask(self, message: str) -> str:
        # 1) Tokenize user query into a unique set of lowercase words.
        query = set(message.lower().split())
        best = None
        best_score = 0

        # 2) Score every policy document by simple token overlap.
        for doc in POLICIES:
            tokens = set((doc["title"] + " " + doc["content"]).lower().split())
            score = len(query & tokens)
            if score > best_score:
                best_score = score
                best = doc

        # 3) Return best match or fallback when nothing is relevant.
        if not best:
            return "No relevant policy found."
        return f"{best['title']}: {best['content']}"
