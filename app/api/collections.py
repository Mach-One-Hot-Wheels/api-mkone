from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_collections():
    return "Hello, collections!"

@router.get("/{collection_id}")
async def read_collection(collection_id: int):
    return {"collection_id": collection_id}