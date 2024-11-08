from fastapi import APIRouter
from ..services.item_service import get_item
from ..models.item_model import Item

router = APIRouter()

@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    return get_item(item_id)
