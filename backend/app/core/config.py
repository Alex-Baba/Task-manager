import os

from dotenv import load_dotenv
from pydantic import BaseModel

# base class for configuration
class Config(BaseModel):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

# function that returns the config class after .env load
def get_config():
    load_dotenv()
    return Config(
        database_url=os.getenv('DATABASE_URL',
                               'sqlite:///db.sqlite3'),
        secret_key=os.getenv('SECRET_KEY', 'change-me-in-production'),
        algorithm=os.getenv('ALGORITHM', 'HS256'),
        access_token_expire_minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30')),
    )
