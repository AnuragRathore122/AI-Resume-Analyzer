import re


def extract_keywords(text):
    text = text.lower()

    words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9+#.-]+\b', text)

    stop_words = {
        "the", "and", "for", "with", "from",
        "that", "this", "have", "will",
        "your", "you", "are", "our",
        "job", "role", "candidate"
    }

    keywords = {
        word
        for word in words
        if len(word) > 2 and word not in stop_words
    }

    return keywords


def calculate_ats_score(resume_text, jd_text):

    resume_keywords = extract_keywords(resume_text)

    jd_keywords = extract_keywords(jd_text)

    if len(jd_keywords) == 0:
        return 0, [], []

    matched = resume_keywords.intersection(jd_keywords)

    missing = jd_keywords - resume_keywords

    score = int(
        (len(matched) / len(jd_keywords)) * 100
    )

    return score, list(matched), list(missing)