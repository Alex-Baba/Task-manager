from datetime import datetime, timezone

def calculate_days_until_due(due_date) -> int | None:
    if due_date is None:
        return None

    now = datetime.now(timezone.utc)

    if due_date.tzinfo is None:
        due_date = due_date.replace(tzinfo=timezone.utc)

    return (due_date - now).days