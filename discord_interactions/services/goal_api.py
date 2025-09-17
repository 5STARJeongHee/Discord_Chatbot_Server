import httpx
from config.properties import BASE_URL

async def fetch_goals(user_id: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/goals?user_id={user_id}")
        if resp.status_code == 200:
            return resp.json()
        return []


async def fetch_goal_detail(goal_uuid: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/goals/{goal_uuid}")
        return resp.json()


async def create_goal(data: dict):
    async with httpx.AsyncClient() as client:
        await client.post(f"{BASE_URL}/goals", json=data)


async def update_goal(goal_uuid: str, data: dict):
    async with httpx.AsyncClient() as client:
        await client.patch(f"{BASE_URL}/goals/{goal_uuid}", json=data)


async def delete_goal(goal_uuid: str):
    async with httpx.AsyncClient() as client:
        await client.delete(f"{BASE_URL}/goals/{goal_uuid}")


async def start_study(goal_uuid: str):
    async with httpx.AsyncClient() as client:
        await client.post(f"{BASE_URL}/goals/{goal_uuid}/study_history/start")


async def end_study(goal_uuid: str):
    async with httpx.AsyncClient() as client:
        await client.patch(f"{BASE_URL}/goals/{goal_uuid}/study_history/end")
