from dotenv import load_dotenv
import os

load_dotenv()

# Database Settings
MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = "health_tracker"

# OpenAI Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_VERSION = os.getenv("API_VERSION")
API_ENDPOINT = os.getenv("API_ENDPOINT")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

# Other Settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# Sentry
SENTRY_DSN = os.getenv("SENTRY_DSN")
