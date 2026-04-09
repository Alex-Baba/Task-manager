import os

from dotenv import load_dotenv
from pydantic import BaseModel

# base class for configuration
class Config(BaseModel):
    database_url: str

# function that returns the config class after .env load
def get_config():
    load_dotenv()
    return Config(
        database_url=os.getenv('DATABASE_URL',
                               'sqlite:///db.sqlite3'),
    )