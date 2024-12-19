from fastapi import FastAPI
from app.routers.whatsapp_flows import router as whatsapp_router
from dotenv import load_dotenv

# Add this at the start of your application
load_dotenv()

app = FastAPI()

# Incluir rutas
app.include_router(whatsapp_router, prefix="/api/v1", tags=["whatsapp"])
