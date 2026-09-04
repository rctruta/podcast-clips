from podcast_clips.captions import dedupe_cues, get_transcript, parse_vtt, to_seconds

# Mimics YouTube's real rolling-window cue structure at minimal scale:
# each finalized line is echoed across 2 cues before the window advances,
# with a karaoke (<c>-tagged) line growing in between.
FIXTURE_VTT = """WEBVTT
Kind: captions
Language: en

00:00:01.000 --> 00:00:02.000 align:start position:0%
Hi<00:00:01.500><c> there</c>

00:00:02.000 --> 00:00:03.000 align:start position:0%
Hi there

00:00:03.000 --> 00:00:04.000 align:start position:0%
Hi there
&gt;&gt; Joe: Welcome<00:00:03.500><c> everyone</c>

00:00:04.000 --> 00:00:05.000 align:start position:0%
Hi there
&gt;&gt; Joe: Welcome everyone

00:00:05.000 --> 00:00:06.000 align:start position:0%
&gt;&gt; Joe: Welcome everyone
&gt;&gt; Ramona Smith: What's<00:00:05.500><c> up</c>

00:00:06.000 --> 00:00:07.000 align:start position:0%
&gt;&gt; Ramona Smith: What's up
"""


def test_to_seconds():
    assert to_seconds("00:01:02.500") == 62.5
    assert to_seconds("01:00:00.000") == 3600.0


def test_parse_vtt_skips_header():
    cues = parse_vtt(FIXTURE_VTT)
    assert len(cues) == 6
    assert cues[0][0] == "00:00:01.000"


def test_dedupe_cues_emits_each_finalized_line_once():
    cues = parse_vtt(FIXTURE_VTT)
    lines = dedupe_cues(cues)
    texts = [t for _, t in lines]
    assert texts == ["Hi there", ">> Joe: Welcome everyone", ">> Ramona Smith: What's up"]


def test_dedupe_cues_timestamps_at_first_finalized_appearance():
    cues = parse_vtt(FIXTURE_VTT)
    lines = dedupe_cues(cues)
    starts = [ts for ts, _ in lines]
    assert starts == [2.0, 4.0, 6.0]


def test_get_transcript_from_file(tmp_path):
    p = tmp_path / "sample.vtt"
    p.write_text(FIXTURE_VTT)
    lines = get_transcript(p)
    assert len(lines) == 3
