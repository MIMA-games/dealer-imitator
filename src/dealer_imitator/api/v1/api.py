from fastapi import APIRouter
from .endpoints.blackjack import router as blackjack_router
from .endpoints.baccarat import router as baccarat_router
from .endpoints.casino_poker import router as casino_poker_router 


router = APIRouter()
router.include_router(blackjack_router, prefix="/blackjack", tags=["blackjack"])
router.include_router(baccarat_router, prefix="/baccarat", tags=["baccarat"])
router.include_router(casino_poker_router, prefix="/casino_poker", tags=["casino_poker"])


@router.get("/health", tags=["general"])
async def health_check():
    return {"message": "success"}
