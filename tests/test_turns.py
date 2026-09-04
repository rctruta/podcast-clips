from podcast_clips.turns import build_turns, filter_by_speaker, has_speaker_tags, video_link

TRANSCRIPT_TAGGED = [
    (2.0, "Hi there"),
    (4.0, ">> Joe: Welcome everyone"),
    (6.0, ">> Ramona Smith: What's up"),
]

TRANSCRIPT_UNTAGGED = [
    (2.0, "Hi there"),
    (4.0, "Welcome everyone"),
]


def test_build_turns_splits_on_tags():
    turns = build_turns(TRANSCRIPT_TAGGED)
    assert len(turns) == 2
    assert turns[0].speaker == "Joe"
    assert turns[0].start == 4.0
    assert turns[0].text == "Welcome everyone"
    assert turns[1].speaker == "Ramona Smith"
    assert turns[1].text == "What's up"


def test_build_turns_no_tags_gives_no_turns():
    assert build_turns(TRANSCRIPT_UNTAGGED) == []


def test_has_speaker_tags():
    assert has_speaker_tags(TRANSCRIPT_TAGGED) is True
    assert has_speaker_tags(TRANSCRIPT_UNTAGGED) is False


def test_filter_by_speaker_is_case_insensitive_substring():
    turns = build_turns(TRANSCRIPT_TAGGED)
    matches = filter_by_speaker(turns, "ramona")
    assert len(matches) == 1
    assert matches[0].speaker == "Ramona Smith"


def test_video_link_format():
    assert video_link("abc123", 90.7) == "https://www.youtube.com/watch?v=abc123&t=90s"
