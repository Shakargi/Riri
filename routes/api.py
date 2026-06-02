from fastapi import APIRouter

from .ping import router as ping_router
from .chat import router as chat_router
from .memory import router as memory_router

api_router = APIRouter()

api_router.include_router(ping_router, tags=["Ping"])
api_router.include_router(chat_router, prefix="/chat", tags=["Chat"])
api_router.include_router(memory_router, prefix="/memory", tags=["Memory"])