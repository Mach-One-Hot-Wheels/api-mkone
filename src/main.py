from fastapi import FastAPI
from src.auth.router import router as auth_router
from src.hotwheels.router import router as hotwheels_router
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


if __name__ == "__main__":
    uvicorn.run("src.main:app")
