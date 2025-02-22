import os

from dotenv import load_dotenv

load_dotenv()

def db_uri() -> str:
    value = os.environ.get("DB_URI")
    if value:
        return value

    raise ValueError("Environment variable 'DB_URI' is missing")
