from fastapi import APIRouter
from .room import router as room
router = APIRouter()

router.include_router(room,prefix="/room")