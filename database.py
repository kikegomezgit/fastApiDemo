from motor.motor_asyncio import AsyncIOMotorClient
from os import getenv
import asyncio
from urllib.parse import urlparse

class MongoDB:
    client: AsyncIOMotorClient = None
    database = None

mongodb = MongoDB()

def extract_database_name_from_uri(uri: str) -> str:
    """Extract database name from MongoDB URI"""
    try:
        parsed = urlparse(uri)
        # Remove leading slash and any query parameters
        db_name = parsed.path.lstrip('/').split('?')[0]
        if db_name:
            return db_name
        else:
            # If no database in URI, use default
            return "fastapi_db"
    except Exception:
        # Fallback to default database name
        return "fastapi_db"

async def connect_to_mongo():
    """Create database connection"""
    mongo_uri = getenv("MONGODB_URI")
    if not mongo_uri:
        raise ValueError("MONGODB_URI environment variable is required")
    
    mongodb.client = AsyncIOMotorClient(mongo_uri)
    
    # Extract database name from URI
    database_name = extract_database_name_from_uri(mongo_uri)
    mongodb.database = mongodb.client[database_name]
    
    # Test the connection
    try:
        await mongodb.client.admin.command('ping')
        print(f"Connected to MongoDB! Using database: {database_name}")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close database connection"""
    if mongodb.client:
        mongodb.client.close()
        print("Disconnected from MongoDB!")

def get_database():
    """Get database instance"""
    return mongodb.database