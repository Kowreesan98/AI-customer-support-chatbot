from fastapi import APIRouter

from app.routes.chat import router as chat_router
from app.routes.health import router as health_router
from app.routes.logs import router as logs_router
from app.routes.upload import router as upload_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
api_router.include_router(upload_router, prefix="/upload", tags=["upload"])
api_router.include_router(logs_router, prefix="/logs", tags=["logs"])


