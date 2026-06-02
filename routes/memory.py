from fastapi import APIRouter
from services.memory_service import MemoryService

memoryService = MemoryService()
router = APIRouter()


@router.get("/")
async def get_memories():
    memories = await memoryService.get_important_memories()

    return {
        "status": "success",
        "data": memories
    }