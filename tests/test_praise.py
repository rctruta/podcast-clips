from podcast_clips.praise import has_praise


def test_detects_real_examples_from_txnikzyhpl4():
    assert has_praise("I mean I love nerdy questions so you know, go for") is True
    assert has_praise("Yeah, absolutely that that's a I love the question.") is True


def test_plain_statement_has_no_praise():
    assert has_praise("So postgres is inherently a row oriented database.") is False


def test_case_insensitive():
    assert has_praise("GREAT QUESTION, let me think.") is True
