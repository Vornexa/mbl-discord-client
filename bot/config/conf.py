import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")

COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"