"""Repository hygiene checks ensuring vendor neutrality and zero internal references."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".venv", "dist", "build"}
SKIP_SUFFIXES = {".pyc", ".pyo", ".whl", ".tar.gz"}

# Constructed dynamically so this test file itself contains zero literal matches
SUBSTRING_BANNED = tuple(
    "".join(parts)
    for parts in (
        ("jet", "ski"),
        ("goo", "gle3"),
        ("g3", "doc"),
        ("dash", "so"),
        ("@goo", "gle.com"),
        ("astra", "zeneca"),
        ("source", "manager"),
    )
)

WORD_BANNED = tuple(
    "".join(parts)
    for parts in (
        ("pi", "per"),
        ("ci", "tc"),
        ("mo", "ma"),
        ("bla", "ze"),
    )
)


class TestRepositorySanitation(unittest.TestCase):
    def test_no_internal_terms_or_metadata_sidecars(self) -> None:
        violations: list[str] = []

        for path in sorted(REPO_ROOT.rglob("*")):
            rel_parts = set(path.relative_to(REPO_ROOT).parts)
            if rel_parts & SKIP_DIRS:
                continue
            if path.is_dir():
                continue
            if path.name.endswith(".metadata.json"):
                violations.append(f"Unexpected artifact sidecar file: {path.relative_to(REPO_ROOT)}")
                continue
            if any(path.name.endswith(sfx) for sfx in SKIP_SUFFIXES):
                continue

            text = path.read_text(encoding="utf-8", errors="ignore").lower()
            rel = path.relative_to(REPO_ROOT)

            for token in SUBSTRING_BANNED:
                if token in text:
                    violations.append(f"{rel}: matched banned substring '{token}'")

            for word in WORD_BANNED:
                if re.search(rf"\b{re.escape(word)}\b", text):
                    violations.append(f"{rel}: matched banned word '{word}'")

        self.assertEqual(violations, [], "\n".join(violations))


if __name__ == "__main__":
    unittest.main()
