from fastapi.responses import JSONResponse
from external.goal_api import edit_goal_api, delete_goal_api

async def handle_edit_goal(payload):
    user = payload["member"]["user"]
    custom_id = payload["data"]["custom_id"]
    goal_id = custom_id.replace("edit_goal_", "")

    default_values = {
        "name": "수정할 목표",
        "category": "카테고리",
        "total_goal": 100,
        "current_progress": 0,
        "unit": "시간",
        "user": user["id"]
    }
    await edit_goal_api(goal_id, default_values)

    return JSONResponse(content={"type": 4, "data": {"content": f"✅ 목표 `{goal_id}` 수정 처리 완료."}})


async def handle_delete_goal(payload):
    custom_id = payload["data"]["custom_id"]
    goal_id = custom_id.replace("delete_goal_", "")

    await delete_goal_api(goal_id)

    return JSONResponse(content={"type": 4, "data": {"content": f"🗑️ 목표 `{goal_id}` 삭제 완료."}})


async def handle_start_goal(payload):
    custom_id = payload["data"]["custom_id"]
    goal_id = custom_id.replace("start_goal_", "")

    return JSONResponse(content={"type": 4, "data": {"content": f"🚀 목표 `{goal_id}` 학습 시작!"}})
