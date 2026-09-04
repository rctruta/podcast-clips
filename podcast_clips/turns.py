"""Split a deduped transcript into speaker turns, using inline live-captioner
tags (">> Name: ...") where present.

Only applies to episodes with a manual/live-captioned track -- plain ASR
transcripts carry no tags and need the classification pipeline instead
(see BRIEF.md's rules/embeddings/LLM tiers).
"""

import html
import re
from dataclasses import dataclass

TAG_RE = re.compile(r">>\s*([^:]{2,40}):")


@dataclass
class Turn:
    speaker: str
    start: float
    text: str


def build_turns(transcript: list[tuple[float, str]]) -> list[Turn]:
    """transcript: list of (timestamp, line) from captions.get_transcript()."""
    full_text = ""
    offsets: list[tuple[int, float]] = []
    for ts, text in transcript:
        offsets.append((len(full_text), ts))
        full_text += text + " "

    matches = list(TAG_RE.finditer(full_text))

    def ts_at(pos: int) -> float:
        best = 0.0
        for off, ts in offsets:
            if off <= pos:
                best = ts
            else:
                break
        return best

    turns = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        speaker = html.unescape(m.group(1)).strip()
        text = html.unescape(full_text[m.end():end]).strip()
        turns.append(Turn(speaker=speaker, start=ts_at(m.start()), text=text))
    return turns


def has_speaker_tags(transcript: list[tuple[float, str]]) -> bool:
    full_text = " ".join(text for _, text in transcript)
    return TAG_RE.search(html.unescape(full_text)) is not None


def filter_by_speaker(turns: list[Turn], name_substring: str) -> list[Turn]:
    needle = name_substring.lower()
    return [t for t in turns if needle in t.speaker.lower()]


def video_link(video_id: str, start: float) -> str:
    return f"https://www.youtube.com/watch?v={video_id}&t={int(start)}s"
