from fastapi import APIRouter
from .endpoints.games import router as game_router


router = APIRouter()
router.include_router(game_router, prefix="/games", tags=["games"])


@router.get("/health", tags=["general"])
async def health_check():
    return {"message": "success"}
