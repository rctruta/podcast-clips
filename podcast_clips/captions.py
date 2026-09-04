"""Collapse YouTube's rolling-window auto-caption VTT into clean, deduped lines.

YouTube ASR captions ship as overlapping cue windows where each new cue
repeats the last 1-3 already-finalized lines plus one growing (karaoke,
<c>-tagged) line. This walks cues in order and emits each finalized line
exactly once, timestamped at the cue where it first appears finalized.
"""

import html
import re
from pathlib import Path

CUE_START_RE = re.compile(r"(\d\d:\d\d:\d\d\.\d+)\s*-->")


def parse_vtt(text: str) -> list[tuple[str, list[str]]]:
    """Split raw VTT text into (start_timestamp, lines) cues."""
    cues = []
    for block in text.split("\n\n"):
        lines = block.strip("\n").split("\n")
        if not lines:
            continue
        m = CUE_START_RE.match(lines[0])
        if not m:
            continue
        cues.append((m.group(1), lines[1:]))
    return cues


def to_seconds(ts: str) -> float:
    h, m, s = ts.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def dedupe_cues(cues: list[tuple[str, list[str]]]) -> list[tuple[float, str]]:
    """Emit each finalized (non-blank, non-karaoke) line once, at first appearance."""
    out = []
    prev_finalized: list[str] = []
    for start, lines in cues:
        finalized = [l for l in lines if l.strip() and "<c" not in l]
        new_lines = [l for l in finalized if l not in prev_finalized]
        for l in new_lines:
            out.append((to_seconds(start), html.unescape(l.strip())))
        prev_finalized = finalized
    return out


def get_transcript(vtt_path: Path) -> list[tuple[float, str]]:
    return dedupe_cues(parse_vtt(vtt_path.read_text()))
