from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId
from typing import List
import os

from database import connect_to_mongo, close_mongo_connection, get_database
from models import ItemCreate, ItemResponse, ItemUpdate

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

# Create FastAPI app
app = FastAPI(
    title="FastAPI MongoDB Demo",
    description="A simple FastAPI application with MongoDB integration",
    version="1.0.0",
    lifespan=lifespan
)

# Helper function to convert ObjectId to string
def item_helper(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "description": item.get("description"),
        "price": item.get("price"),
        "category": item.get("category"),
        "created_at": item["created_at"]
    }

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "FastAPI with MongoDB is running!"}

@app.get("/items", response_model=List[ItemResponse])
async def get_items():
    """Get all items from the database"""
    try:
        db = get_database()
        items = []
        async for item in db.items.find():
            items.append(item_helper(item))
        return items
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching items: {str(e)}"
        )

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    """Get a single item by ID"""
    try:
        # Validate ObjectId format
        if not ObjectId.is_valid(item_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid item ID format"
            )
        
        db = get_database()
        item = await db.items.find_one({"_id": ObjectId(item_id)})
        
        if item:
            return item_helper(item)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching item: {str(e)}"
        )

@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    """Create a new item"""
    try:
        db = get_database()
        
        # Prepare item data
        item_data = item.dict()
        item_data["created_at"] = datetime.utcnow()
        
        # Insert item into database
        result = await db.items.insert_one(item_data)
        
        # Fetch the created item
        created_item = await db.items.find_one({"_id": result.inserted_id})
        
        return item_helper(created_item)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating item: {str(e)}"
        )

@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: str, item: ItemUpdate):
    """Update an existing item"""
    try:
        # Validate ObjectId format
        if not ObjectId.is_valid(item_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid item ID format"
            )
        
        db = get_database()
        
        # Get only non-None values for update
        update_data = {k: v for k, v in item.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields provided for update"
            )
        
        # Update item
        result = await db.items.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
        
        # Fetch updated item
        updated_item = await db.items.find_one({"_id": ObjectId(item_id)})
        return item_helper(updated_item)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating item: {str(e)}"
        )

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    """Delete an item"""
    try:
        # Validate ObjectId format
        if not ObjectId.is_valid(item_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid item ID format"
            )
        
        db = get_database()
        result = await db.items.delete_one({"_id": ObjectId(item_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
        
        return {"message": "Item deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting item: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )

    