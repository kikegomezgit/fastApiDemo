from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ItemCreate(BaseModel):
    """Model for creating a new item"""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the item")
    description: Optional[str] = Field(None, max_length=500, description="Description of the item")
    price: Optional[float] = Field(None, ge=0, description="Price of the item")
    category: Optional[str] = Field(None, max_length=50, description="Category of the item")

class ItemResponse(BaseModel):
    """Model for item response"""
    id: str = Field(..., alias="_id")
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    created_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ItemUpdate(BaseModel):
    """Model for updating an item"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=50)