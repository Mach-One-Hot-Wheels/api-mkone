from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_wishlist():
    return {"wishlist": "wishlist"}