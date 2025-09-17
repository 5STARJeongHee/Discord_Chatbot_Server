from fastapi.responses import JSONResponse
from discord_interactions.services import goal_api

async def handle_modal(payload: dict):
    custom_id = payload.get("data", {}).get("custom_id")
    components = payload.get("data", {}).get("components", [])

    values = {}
    for row in components:
        for comp in row.get("components", []):
            values[comp["custom_id"]] = comp.get("value")

    if custom_id == "modal_register_goal":
        await goal_api.create_goal(values)
        return JSONResponse(content={
            "type": 4,
            "data": {"content": "✅ 목표가 등록되었습니다."}
        })

    if custom_id.startswith("modal_edit_goal:"):
        goal_uuid = custom_id.split(":")[1]
        await goal_api.update_goal(goal_uuid, values)
        return JSONResponse(content={
            "type": 4,
            "data": {"content": "✏️ 목표가 수정되었습니다."}
        })
