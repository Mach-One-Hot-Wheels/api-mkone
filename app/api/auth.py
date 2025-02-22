from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_auth():
    return "Hello, users!"