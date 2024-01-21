from fastapi import APIRouter
from .endpoints.blackjack import router as game_router


router = APIRouter()
router.include_router(game_router, prefix="/blackjack", tags=["blackjack"])


@router.get("/health", tags=["general"])
async def health_check():
    return {"message": "success"}
