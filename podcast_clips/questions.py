"""Tier-1 (rules) question detector -- the cheapest tier in BRIEF.md's method.

Deliberately narrow. An earlier pass matched generic question words (how,
what, do you, ...) anywhere in a turn and got swamped by false positives:
answers routinely contain "how"/"you want" while explaining something.
That approach is not used here -- see test_questions.py::test_rejects_generic_question_words_in_answers
for the case that killed it.

This only flags: a literal "?", or a small set of self-referential
question-announcing phrases ("my question is", "I wanted to ask", ...).
High precision, low recall by design -- it will miss questions with no
"?" and no self-labeling. That gap is exactly what the embedding/LLM
tiers exist to close; measure against hand-labeled turns before trusting
this alone.
"""

import re

SELF_LABEL_RE = re.compile(
    r"\bmy question\b|\bi have a question\b|\bi wanted to ask\b|"
    r"\bi want(?:ed)? to ask\b|\bquick question\b|\bi('m| am) wondering\b",
    re.IGNORECASE,
)


def is_question(text: str) -> bool:
    if "?" in text:
        return True
    return bool(SELF_LABEL_RE.search(text))
