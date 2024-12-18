from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.whatsapp import process_whatsapp_request

router = APIRouter()

class WhatsAppRequest(BaseModel):
    encrypted_aes_key: str
    encrypted_flow_data: str
    initial_vector: str

@router.post("/")
async def whatsapp_flows(request: WhatsAppRequest):
    try:
        response = process_whatsapp_request(request.dict())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
