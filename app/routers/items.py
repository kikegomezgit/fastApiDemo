from fastapi import APIRouter, HTTPException, status
from typing import List
from app.services.item_service import ItemService
from app.models.item import ItemCreate, ItemUpdate, ItemResponse

# Create router instance
router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

# Initialize service
item_service = ItemService()

@router.get("/", response_model=List[ItemResponse])
async def get_items():
    """Get all items from the database"""
    try:
        return await item_service.get_all_items()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching items: {str(e)}"
        )

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    """Get a single item by ID"""
    try:
        item = await item_service.get_item_by_id(item_id)
        
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
        
        return item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching item: {str(e)}"
        )

@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    """Create a new item"""
    try:
        return await item_service.create_item(item)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating item: {str(e)}"
        )

@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: str, item: ItemUpdate):
    """Update an existing item"""
    try:
        updated_item = await item_service.update_item(item_id, item)
        
        if not updated_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found or no valid fields provided for update"
            )
        
        return updated_item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating item: {str(e)}"
        )

@router.delete("/{item_id}")
async def delete_item(item_id: str):
    """Delete an item"""
    try:
        deleted = await item_service.delete_item(item_id)
        
        if not deleted:
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