import motor.motor_asyncio
from app.utils.settings import MONGO_URL
from dotenv import load_dotenv

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.health_tracker
