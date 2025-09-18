from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.blockchain_route import router as blockchain_router

app = FastAPI(
    title="HLX Blockchain API",
    description="An API to fetch live stats from the custom HLX blockchain node.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(blockchain_router, prefix="/api")