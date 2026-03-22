import os
import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

# We can fall back to local mongodb if MONGODB_URI is not set
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "phishing_detection")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
db = client[DB_NAME]

async def init_db():
    # Attempt to create indexes
    collection = db.scan_history
    await collection.create_index("timestamp")
    await collection.create_index("scan_type")

async def get_db():
    return db
