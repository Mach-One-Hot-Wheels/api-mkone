from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import users, hotwheels, collections, wishlists

app = FastAPI(title="Mach One Hot Wheels API")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(hotwheels.router, prefix="/api/hotwheels", tags=["hotwheels"])
app.include_router(collections.router, prefix="/api/collections", tags=["collections"])
app.include_router(wishlists.router, prefix="/api/wishlists", tags=["wishlists"])