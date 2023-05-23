from os import getenv
from dotenv import load_dotenv, find_dotenv
from typing import Tuple, TypeVar

__all__ = [
    "Auth",
    "BotSettings"
]

load_dotenv(find_dotenv())

class Auth:
    TOKEN: str = getenv("TOKEN")
    COMMAND_PREFIX: str = getenv("COMMAND_PREFIX")
    DB_HOST: str = getenv("DB_HOST")
    DB_PORT: int = getenv("DB_PORT")
    DB_USER: str = getenv("DB_USER")
    DB_PASSWD: str = getenv("DB_PASSWD")
    DB_NAME: str = getenv("DB_NAME")

class BotSettings:
    # DEFAULT VALUES
    EMBED_COLOR: int = 0xffa500
    EMBED_ERROR_COLOR: int = 0xff0000
    EMBED_TIMESTAMP: bool = False
    
    profile: str = "profile"
    union_raid: str = "union_raid"
    ur_profiles: str = "ur_profiles"
    gs: str = "gs"
    notifs: str = "notifs"
