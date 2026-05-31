from fastapi import APIRouter
from .chat import router as chat_router
from .ping import router as ping_router

api_router = APIRouter()

api_router.include_router(ping_router)
api_router.include_router(chat_router, prefix="/chat")