from textstats.words import word_count, top_words


def test_word_count():
    assert word_count("a b c") == 3


def test_top_words():
    assert top_words("a a b", 2)[0] == "a"
