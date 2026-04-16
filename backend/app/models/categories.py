from enum import Enum


class Category(str,Enum):
    WORK = 'WORK'
    PERSONAL = 'PERSONAL'
    SHOPPING = 'SHOPPING'
    HEALTH = 'HEALTH'
    FINANCE = 'FINANCE'
    EDUCATION = 'EDUCATION'
    ENTERTAINMENT = 'ENTERTAINMENT'
    OTHER = 'OTHER'


