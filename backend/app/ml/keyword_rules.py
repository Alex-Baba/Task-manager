URGENT_KEYWORDS = {
    "urgent",
    "asap",
    "critic",
    "critical",
    "imediat",
    "important",
    "deadline",

    # English
    "emergency",
    "high priority",
    "priority",
    "blocker",
    "blocking",
    "hotfix",
    "immediately",
    "right away",
    "time-sensitive",
    "rush",
    "expedite",
    "must",
    "needs attention",
    "action required",
    "urgent issue",
    "production issue",
    "prod issue",
    "outage",
    "sev1",
    "sev2",
    "p1",
    "p0",

    # Romanian
    "urgentă",
    "urgent!",
    "rapid",
    "repede",
    "foarte important",
    "cat mai repede",
    "cât mai repede",
    "acum",
    "prioritar",
    "blocant",
    "problemă critică",
    "incident",
    "eroare gravă",
    "nu merge",
    "picat",
}

def calculate_keyword_score(text: str) -> tuple[float, list[str]]:
    text_lower = text.lower()
    matched = [word for word in URGENT_KEYWORDS if word in text_lower]

    if not matched:
        return 0.0, []

    score = min(len(matched) * 0.2, 1.0)
    return score, matched