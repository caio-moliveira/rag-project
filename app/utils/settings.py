import os
from platform import system
from dotenv import load_dotenv, find_dotenv


class Settings:
    load_dotenv()

    ENV_FILE = find_dotenv()
    SYSTEM = system()

    QDRANT_HOST = "localhost"
    QDRANT_PORT = "6333"


settings = Settings()
