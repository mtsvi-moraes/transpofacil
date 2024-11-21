from fastapi import APIRouter, HTTPException
from ..services.olhovivo_service import OlhoVivoService
from ..services import item_service, genai_service
from ..models.item_model import Item
from ..schemas.input_text import InputText

router = APIRouter()
olho_vivo_service = OlhoVivoService()



@router.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    item = item_service.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/generate-response/")
def generate_response(termos_busca: str = "Jurubatuba"):
    try:
        linhas = olho_vivo_service.buscar_linhas(termos_busca=termos_busca)
        response = olho_vivo_service.gerar_resposta(linhas)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))