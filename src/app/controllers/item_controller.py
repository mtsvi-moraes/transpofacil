from fastapi import APIRouter, HTTPException
from ..services import item_service, genai_service
from ..models.item_model import Item
from ..schemas.input_text import InputText

router = APIRouter()



@router.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    item = item_service.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/generate-response/")
def generate_response(input_text: InputText):
    response = genai_service.get_response(input_text.input_text)
    return {"response": response}
