from fastapi import FastAPI
from app.routers.whatsapp_flows import router as whatsapp_router

app = FastAPI()

app.include_router(whatsapp_router, prefix="/api/v1/whatsapp", tags=["WhatsApp Flows"])
