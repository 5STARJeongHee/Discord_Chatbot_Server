from fastapi.responses import JSONResponse
from discord_interactions.services import goal_api

async def handle_component(payload: dict):
    custom_id = payload.get("data", {}).get("custom_id")

    if custom_id.startswith("help_"):
        return await handle_help_detail(custom_id)

    if custom_id.startswith("goal_detail:"):
        goal_uuid = custom_id.split(":")[1]
        return await handle_goal_detail(goal_uuid)

    if custom_id.startswith("goal_edit:"):
        goal_uuid = custom_id.split(":")[1]
        return await handle_goal_edit(goal_uuid)

    if custom_id.startswith("goal_delete:"):
        goal_uuid = custom_id.split(":")[1]
        return await handle_goal_delete(goal_uuid)

    return JSONResponse(content={
        "type": 4,
        "data": {"content": "⚠️ 알 수 없는 버튼입니다."}
    })


async def handle_help_detail(custom_id: str):
    if custom_id == "help_register_goal":
        return JSONResponse(content={
            "type": 4,
            "data": {"content": "📖 `/register_goal` 명령어는 목표 등록을 위한 입력폼을 엽니다."}
        })
    if custom_id == "help_view_goal":
        return JSONResponse(content={
            "type": 4,
            "data": {"content": "📖 `/view_goal` 명령어는 목표 목록을 보여주고, 세부 내용을 확인할 수 있습니다."}
        })


async def handle_goal_detail(goal_uuid: str):
    goal = await goal_api.fetch_goal_detail(goal_uuid)

    return JSONResponse(content={
        "type": 4,
        "data": {
            "content": f"🎯 {goal['name']} ({goal['category']}) - {goal['progress']}/{goal['total_goal']} {goal['unit']}",
            "components": [
                {
                    "type": 1,
                    "components": [
                        {"type": 2, "style": 1, "label": "수정", "custom_id": f"goal_edit:{goal_uuid}"},
                        {"type": 2, "style": 4, "label": "삭제", "custom_id": f"goal_delete:{goal_uuid}"}
                    ]
                },
                {
                    "type": 1,
                    "components": [
                        {"type": 2, "style": 3, "label": "학습 시작", "custom_id": f"goal_study_start:{goal_uuid}"},
                        {"type": 2, "style": 2, "label": "학습 종료", "custom_id": f"goal_study_end:{goal_uuid}"}
                    ]
                }
            ]
        }
    })


async def handle_goal_edit(goal_uuid: str):
    """목표 수정 모달"""
    return JSONResponse(content={
        "type": 9,
        "data": {
            "title": "목표 수정",
            "custom_id": f"modal_edit_goal:{goal_uuid}",
            "components": [
                {
                    "type": 1,
                    "components": [{
                        "type": 4, "custom_id": "goal_name",
                        "style": 1, "label": "목표 이름"
                    }]
                }
            ]
        }
    })


async def handle_goal_delete(goal_uuid: str):
    await goal_api.delete_goal(goal_uuid)
    return JSONResponse(content={
        "type": 4,
        "data": {"content": f"🗑️ 목표가 삭제되었습니다."}
    })
