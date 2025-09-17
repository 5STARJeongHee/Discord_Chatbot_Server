from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from discord_interactions.routes import router as discord_router
from discord_interactions.handlers import register_commands
import uvicorn

app = FastAPI(title="Study Goals API", version="1.0.0")


app.add_middleware(
CORSMiddleware,
allow_credentials=True,
allow_origins=["*"],
allow_methods=["*"],
allow_headers=["*"],
)

app.include_router(discord_router)

@app.get("/")
async def root():
    return {"message": "Discord Interaction Server is running."}

if __name__ == "__main__":
    register_commands.register_commands()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
