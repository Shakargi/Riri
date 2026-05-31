from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.api import api_router

app = FastAPI(title="Riri API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Riri Server!"}