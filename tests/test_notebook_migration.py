from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "notebooks"


def test_notebooks_exist():
    notebooks = list(NB_DIR.glob("*.ipynb"))
    assert len(notebooks) >= 4


def test_no_airline_system_prompt_phrase():
    # Keep this check narrow to avoid false positives in benchmark references.
    for nb in NB_DIR.glob("*.ipynb"):
        text = nb.read_text(encoding="utf-8")
        assert "You are a virtual airline assistant." not in text


def test_retail_policy_corpus_present():
    seminar = next(
        nb for nb in NB_DIR.glob("*.ipynb") if "Memory and Guardrails" in nb.name
    )
    text = seminar.read_text(encoding="utf-8")
    assert "Retail policy handbook" in text
    assert "Return Window" in text
