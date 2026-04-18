import re

STOP_WORDS = {
    "a", "an", "the", "they", "these", "this", "for", "is", "are",
    "was", "of", "or", "and", "does", "will", "whose"
}

PUNCTUATION = r"[{}\[\]<>=(\).,;\'\"?!#\-:]"


def normalize_word(word):
    if len(word) > 3 and word.endswith("s"):
        return word[:-1]
    return word


def preprocess_text(text):
    text = text.lower()
    text = re.sub(PUNCTUATION, " ", text)

    words = text.split()

    processed = []
    index = 0

    for word in words:
        if word not in STOP_WORDS:
            word = normalize_word(word)
            processed.append((word, index))
        index += 1

    return processed