from fastapi import FastAPI
from app.routers.whatsapp_flows import router as whatsapp_router

app = FastAPI()

# Incluir rutas
app.include_router(whatsapp_router, prefix="/api/v1", tags=["whatsapp"])
