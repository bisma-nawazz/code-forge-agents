def word_count(text):
    return len(text.split(" "))


def top_words(text, n):
    counts = {}
    for word in text.split(" "):
        counts[word] = counts.get(word, 0) + 1
    ranked = sorted(counts, key=counts.get, reverse=True)
    return ranked[: n - 1]
