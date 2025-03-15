from fastapi import FastAPI
from src.auth.router import router as auth_router
from src.hotwheels.router import router as hotwheels_router
from src.collections.router import router as collections_router
from src.user_hotwheels.router import router as user_hotwheels_router
from src.wishlist.router import router as wishlist_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(hotwheels_router, prefix="/hotwheels", tags=["hotwheels"])
app.include_router(collections_router, prefix="/collections", tags=["collections"])
app.include_router(user_hotwheels_router, prefix="/user_hotwheels", tags=["user_hotwheels"])
app.include_router(wishlist_router, prefix="/wishlist_router", tags=["wishlist_router"])


if __name__ == "__main__":
    uvicorn.run("src.main:app")
