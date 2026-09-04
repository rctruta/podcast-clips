from podcast_clips.questions import is_question


def test_literal_question_mark():
    assert is_question("How much faster is ADBC than ODBC?") is True


def test_self_labeled_question_with_no_question_mark():
    # Real turn from TXNIkzYhPL4 (Ramona, 3054s) -- no "?", but explicitly
    # self-labels as a question. A generic question-word regex missed this
    # entirely in the first pass; this is the case that motivated adding
    # SELF_LABEL_RE.
    text = (
        "Yes, first of all impressive, talk like the automation that "
        "animation. Sorry think created for everyone a very clear mental "
        "model my question is a little bit, maybe it's very specific."
    )
    assert is_question(text) is True


def test_rejects_generic_question_words_in_answers():
    # Real turn from TXNIkzYhPL4 (Ian Cook, 2126s) -- contains "you want"
    # but is not a question, it's an offer/statement. The rejected first-pass
    # heuristic (matching "what|why|how|do you|can you|..." anywhere) flagged
    # this as a question; it isn't one.
    text = "You want me to share a bill?"
    # (this one legitimately has a "?" so it IS flagged -- kept as a reminder
    # that "?" alone is not perfectly precise either, just much better than
    # bare question-word matching)
    assert is_question(text) is True

    non_question_with_question_word = (
        "So if you want to use Adbc, the first step is installing drivers."
    )
    assert is_question(non_question_with_question_word) is False


def test_plain_statement_is_not_a_question():
    assert is_question("Thanks so much for having us Joe.") is False
