from fastapi.responses import JSONResponse
from discord_interactions.services import goal_api

async def handle_slash_command(payload: dict):
    command_name = payload.get("data", {}).get("name")

    if command_name == "help":
        return await help_command()
    elif command_name == "register_goal":
        return await register_goal_command()
    elif command_name == "view_goal":
        return await view_goal_command(payload)
    else:
        return JSONResponse(content={
            "type": 4,
            "data": {"content": f"⚠️ 알 수 없는 명령어: {command_name}"}
        })


async def help_command():
    return JSONResponse(content={
        "type": 4,
        "data": {
            "content": "📌 사용 가능한 명령어 목록입니다.",
            "components": [
                {
                    "type": 1,  # ActionRow
                    "components": [
                        {
                            "type": 2, "style": 1,
                            "label": "/register_goal - 목표 등록",
                            "custom_id": "help_register_goal"
                        },
                        {
                            "type": 2, "style": 1,
                            "label": "/view_goal - 목표 보기",
                            "custom_id": "help_view_goal"
                        }
                    ]
                }
            ]
        }
    })


async def register_goal_command():
    """목표 등록용 모달 띄우기"""
    print("register_goal_command called")
    return JSONResponse(content={
        "type": 9,
        "data": {
            "title": "🎯 목표 등록",
            "custom_id": "modal_register_goal",
            "components": [
                {
                    "type": 1,
                    "components": [{
                        "type": 4, "custom_id": "goal_name",
                        "style": 1, "label": "목표 이름", "required": True
                    }]
                },
                {
                    "type": 1,
                    "components": [{
                        "type": 4, "custom_id": "goal_category",
                        "style": 1, "label": "카테고리", "required": True
                    }]
                },
                {
                    "type": 1,
                    "components": [{
                        "type": 4, "custom_id": "goal_total",
                        "style": 1, "label": "총 목표량", "required": True
                    }]
                },
                {
    "type": 1,
    "components": [{
        "type": 4,
        "custom_id": "unit",
        "style": 1,  # Short
        "label": "단위 (Count / Time / Day 중 선택)",
        "required": True
    }]
}

            ]
        }
    })


async def view_goal_command(payload: dict):
    """목표 목록 가져오기 (Spring API 연동)"""
    user_id = payload.get("member", {}).get("user", {}).get("id")
    goals = await goal_api.fetch_goals(user_id)

    if not goals:
        return JSONResponse(content={
            "type": 4,
            "data": {"content": "📭 등록된 목표가 없습니다."}
        })

    components = []
    for g in goals:
        components.append({
            "type": 2, "style": 1,
            "label": g["name"],
            "custom_id": f"goal_detail:{g['uuid']}"
        })

    return JSONResponse(content={
        "type": 4,
        "data": {
            "content": "📋 목표 목록:",
            "components": [{"type": 1, "components": components}]
        }
    })
