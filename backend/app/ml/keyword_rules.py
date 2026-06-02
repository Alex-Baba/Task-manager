import re
import unicodedata


KEYWORD_WEIGHTS = {
    "p0": 1.0,
    "sev1": 1.0,
    "critical": 0.9,
    "emergency": 0.9,
    "outage": 0.9,
    "production issue": 0.85,
    "urgent": 0.75,
    "asap": 0.75,
    "immediately": 0.75,
    "blocker": 0.7,
    "blocking": 0.7,
    "hotfix": 0.65,
    "imediat": 0.75,
    "blocant": 0.7,
    "deadline": 0.5,
    "high priority": 0.5,
    "important": 0.3,
    "prioritar": 0.35,
    "cat mai repede": 0.45,
    "cât mai repede": 0.45,
    "rapid": 0.25,
    "repede": 0.25,
    "nu merge": 0.5,
    "picat": 0.6,
}


REGEX_RULES = [
    (r"\bp0\b|\bsev1\b", 1.0),
    (r"\b(prod|production).*(down|issue|outage)\b", 0.9),
    (r"\b(deadline|due)\s+(today|tomorrow)\b", 0.8),
    (r"\bneed(s)?\s+(this|it)?\s*(now|asap)\b", 0.75),
    (r"\b(blocked|blocking|blocker)\b", 0.7),
    (r"\bcat\s+mai\s+repede\b", 0.45),
]


def normalize_text(text: str) -> str:
    text = text.lower()

    text = "".join(
        char
        for char in unicodedata.normalize("NFD", text)
        if unicodedata.category(char) != "Mn"
    )

    return text


def calculate_keyword_score(text: str) -> tuple[float, list[str]]:
    text_normalized = normalize_text(text)

    score = 0.0
    matched = []

    for keyword, weight in KEYWORD_WEIGHTS.items():
        keyword_normalized = normalize_text(keyword)
        pattern = rf"\b{re.escape(keyword_normalized)}\b"

        if re.search(pattern, text_normalized):
            score += weight
            matched.append(keyword)

    return min(score, 1.0), matched


def calculate_regex_score(text: str) -> tuple[float, list[str]]:
    text_normalized = normalize_text(text)

    score = 0.0
    matched = []

    for pattern, weight in REGEX_RULES:
        if re.search(pattern, text_normalized):
            score += weight
            matched.append(pattern)

    return min(score, 1.0), matched


def calculate_urgency_score(text: str) -> dict:
    keyword_score, matched_keywords = calculate_keyword_score(text)
    regex_score, matched_regex = calculate_regex_score(text)

    final_score = keyword_score * 0.65 + regex_score * 0.35

    return {
        "score": round(min(final_score, 1.0), 3),
        "keyword_score": round(keyword_score, 3),
        "regex_score": round(regex_score, 3),
        "matched_keywords": matched_keywords,
        "matched_regex": matched_regex,
    }
