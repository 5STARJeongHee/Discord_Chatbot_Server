# api_server/main.py
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from discord_interactions.routes import router as discord_router

app = FastAPI()

# CORS (필요 시)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Discord Interactions 라우터 등록
app.include_router(discord_router)

@app.get("/")
async def root():
    return {"message": "Discord Interaction Server is running."}
