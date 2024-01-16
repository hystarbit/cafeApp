import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

"""
Start mongodb by `brew services start mongodb-community@5.0`
"""

load_dotenv()

client = AsyncIOMotorClient(os.environ["DB_URI"])