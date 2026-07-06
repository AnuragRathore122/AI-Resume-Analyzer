import re

def extract_keywords(text):

    text = text.lower()

    words = re.findall(
        r'\b[a-zA-Z][a-zA-Z0-9+#.-]+\b',
        text
    )

    stop_words = {
        "the", "and", "for", "with",
        "from", "that", "this",
        "have", "will", "your",
        "you", "are"
    }

    keywords = {
        word
        for word in words
        if len(word) > 2
        and word not in stop_words
    }

    return list(keywords)