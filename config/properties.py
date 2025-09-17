import os
from dotenv import load_dotenv

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8000")
DISCORD_PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")  # Discord Developer Portal에서 제공
BASE_URL = os.getenv("SPRING_API_BASE", "http://114.205.50.113:8093/api")
DISCORD_APP_ID=os.getenv("DISCORD_APP_ID")
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
