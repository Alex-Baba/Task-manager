def build_category_text(task) -> str:
    parts = [
        task.title or "",
        task.description or "",
    ]

    if task.tags:
        parts.append(" ".join(tag.name for tag in task.tags))

    return " ".join(parts).strip()