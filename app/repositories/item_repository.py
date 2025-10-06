from typing import List, Optional
from bson import ObjectId
from datetime import datetime
from app.core.database import get_database
from app.models.item import ItemCreate, ItemUpdate

class ItemRepository:
    def __init__(self):
        self.collection_name = "items"
    
    @property
    def collection(self):
        """Get the items collection"""
        db = get_database()
        return db[self.collection_name]
    
    async def create_item(self, item_data: ItemCreate) -> dict:
        """Create a new item in the database"""
        item_dict = item_data.dict()
        item_dict["created_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(item_dict)
        created_item = await self.collection.find_one({"_id": result.inserted_id})
        return created_item
    
    async def get_item_by_id(self, item_id: str) -> Optional[dict]:
        """Get an item by its ID"""
        if not ObjectId.is_valid(item_id):
            return None
        
        return await self.collection.find_one({"_id": ObjectId(item_id)})
    
    async def get_all_items(self) -> List[dict]:
        """Get all items from the database"""
        items = []
        async for item in self.collection.find():
            items.append(item)
        return items
    
    async def update_item(self, item_id: str, item_data: ItemUpdate) -> Optional[dict]:
        """Update an existing item"""
        if not ObjectId.is_valid(item_id):
            return None
        
        # Get only non-None values for update
        update_data = {k: v for k, v in item_data.dict().items() if v is not None}
        
        if not update_data:
            return None
        
        result = await self.collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            return None
        
        return await self.collection.find_one({"_id": ObjectId(item_id)})
    
    async def delete_item(self, item_id: str) -> bool:
        """Delete an item by its ID"""
        if not ObjectId.is_valid(item_id):
            return False
        
        result = await self.collection.delete_one({"_id": ObjectId(item_id)})
        return result.deleted_count > 0