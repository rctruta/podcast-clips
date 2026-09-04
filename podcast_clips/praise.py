"""Detect praise language directed at a question/point, in the turn that follows it.

Starter lexicon, grown from what actually showed up in TXNIkzYhPL4
("I love nerdy questions", "I love the question", "Nice. Yeah. Thank[s]").
Expect to extend this once more transcripts are in -- treat misses as
data, not bugs, until the corpus says otherwise.
"""

import re

PRAISE_RE = re.compile(
    r"\blove (that|this|the|nerdy) questions?\b|\bgreat questions?\b|"
    r"\bgood questions?\b|\bnice questions?\b|\bgreat point\b|\bgood point\b|"
    r"\bexcellent questions?\b",
    re.IGNORECASE,
)


def has_praise(text: str) -> bool:
    return bool(PRAISE_RE.search(text))
