from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_wishlists():
    return "Hello, wishlists!"