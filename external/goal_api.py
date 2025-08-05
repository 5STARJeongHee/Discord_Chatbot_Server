import httpx
from config.properties import SERVER_URL

async def edit_goal_api(goal_id: str, payload: dict) -> httpx.Response:
    url = f"{SERVER_URL}/api/goals/{goal_id}"
    print(f"Editing goal {goal_id} at {url}")
    async with httpx.AsyncClient() as client:
        return await client.put(url, json=payload)

async def delete_goal_api(goal_id: str) -> httpx.Response:
    url = f"{SERVER_URL}/api/goals/{goal_id}"
    print(f"Deleting goal {goal_id} from {url}")
    async with httpx.AsyncClient() as client:
        return await client.delete(url)

async def view_single_goal_api(goal_id: str) -> httpx.Response:
    url = f"{SERVER_URL}/api/goals/{goal_id}"
    print(f"Fetching goal {goal_id} from {url}")
    async with httpx.AsyncClient() as client:
        return await client.get(url)
    
# external/goal_api.py

async def view_goals_api(user_id: str) -> httpx.Response:
    url = f"{SERVER_URL}/api/goals/list?id={user_id}"
    print(f"Fetching goals for user {user_id} from {url}")
    async with httpx.AsyncClient() as client:
        return await client.get(url)
