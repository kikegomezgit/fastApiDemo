from typing import List, Optional
from app.repositories.item_repository import ItemRepository
from app.models.item import ItemCreate, ItemUpdate, ItemResponse

class ItemService:
    def __init__(self):
        self.item_repository = ItemRepository()
    
    def _item_helper(self, item: dict) -> dict:
        """Convert MongoDB document to response format"""
        return {
            "id": str(item["_id"]),
            "name": item["name"],
            "description": item.get("description"),
            "price": item.get("price"),
            "category": item.get("category"),
            "created_at": item["created_at"]
        }
    
    async def create_item(self, item_data: ItemCreate) -> ItemResponse:
        """Create a new item"""
        created_item = await self.item_repository.create_item(item_data)
        item_dict = self._item_helper(created_item)
        return ItemResponse(**item_dict)
    
    async def get_item_by_id(self, item_id: str) -> Optional[ItemResponse]:
        """Get an item by ID"""
        item = await self.item_repository.get_item_by_id(item_id)
        if not item:
            return None
        
        item_dict = self._item_helper(item)
        return ItemResponse(**item_dict)
    
    async def get_all_items(self) -> List[ItemResponse]:
        """Get all items"""
        items = await self.item_repository.get_all_items()
        return [ItemResponse(**self._item_helper(item)) for item in items]
    
    async def update_item(self, item_id: str, item_data: ItemUpdate) -> Optional[ItemResponse]:
        """Update an existing item"""
        updated_item = await self.item_repository.update_item(item_id, item_data)
        if not updated_item:
            return None
        
        item_dict = self._item_helper(updated_item)
        return ItemResponse(**item_dict)
    
    async def delete_item(self, item_id: str) -> bool:
        """Delete an item"""
        return await self.item_repository.delete_item(item_id)
    
    async def item_exists(self, item_id: str) -> bool:
        """Check if an item exists"""
        item = await self.item_repository.get_item_by_id(item_id)
        return item is not None