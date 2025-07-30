import httpx
from config.properties import SERVER_URL

async def edit_goal_api(goal_id: str, payload: dict) -> httpx.Response:
    url = f"{SERVER_URL}/api/goals/{goal_id}"
    async with httpx.AsyncClient() as client:
        return await client.put(url, json=payload)

async def delete_goal_api(goal_id: str) -> httpx.Response:
    url = f"{SERVER_URL}/api/goals/{goal_id}"
    async with httpx.AsyncClient() as client:
        return await client.delete(url)
