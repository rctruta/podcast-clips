"""End-to-end check against a real saved caption file.

Skips if the fixture isn't present (e.g. a fresh checkout before any
caption has been fetched) rather than failing the suite.
"""

from pathlib import Path

import pytest

from podcast_clips.captions import get_transcript
from podcast_clips.turns import build_turns, filter_by_speaker

REAL_VTT = Path(__file__).parent.parent / "raw_captions" / "TXNIkzYhPL4.en-uYU-mmqFLq8.vtt"

pytestmark = pytest.mark.skipif(not REAL_VTT.exists(), reason="fixture caption file not present")


def test_full_pipeline_turn_and_speaker_counts():
    transcript = get_transcript(REAL_VTT)
    turns = build_turns(transcript)

    assert len(turns) == 48

    speakers = {t.speaker for t in turns}
    assert speakers == {"Ian Cook", "Emil Sadek", "Joe Reis", "Ramona C. Truta", "Matthew Mullins"}

    ramona_turns = filter_by_speaker(turns, "ramona")
    assert len(ramona_turns) == 3
    assert ramona_turns[0].start == pytest.approx(3053.8, abs=1.0)
