from fastapi import FastAPI

from routes.api import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Riri Server")

app.include_router(api_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","https://riri-frontend.vercel.app"],  # Vite's dev server address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Riri's brain"}

