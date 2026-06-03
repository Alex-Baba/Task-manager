from enum import Enum


class Status(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class CategoryEnum(str, Enum):
    WORK = "WORK"
    PERSONAL = "PERSONAL"
    SHOPPING = "SHOPPING"
    HEALTH = "HEALTH"
    FINANCE = "FINANCE"
    EDUCATION = "EDUCATION"
    ENTERTAINMENT = "ENTERTAINMENT"
    OTHER = "OTHER"


class PriorityEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
