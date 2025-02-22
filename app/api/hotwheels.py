from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_hotwheels():
    return "Hello, hotwheels!"