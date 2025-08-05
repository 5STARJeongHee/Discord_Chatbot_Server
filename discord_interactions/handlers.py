from fastapi.responses import JSONResponse
from external.goal_api import edit_goal_api, delete_goal_api, view_single_goal_api, view_goals_api

async def handle_edit_goal(payload):
    user = payload["member"]["user"]
    custom_id = payload["data"]["custom_id"]
    print(f"Handling edit goal with custom_id: {custom_id}")

    if custom_id.startswith("edit_goal_"):
        # 기존 목표 정보 조회
        goal_id = custom_id.replace("edit_goal_", "")
        print(f"Editing goal with custom_id: {custom_id}")
        response = await view_single_goal_api(goal_id)
        if response.status_code != 200:
            return JSONResponse(content={"type": 4, "data": {"content": "❌ 목표 정보를 불러오지 못했습니다."}})

        goal = response.json()

        # Discord Modal 형태로 응답 (type 9)
        modal = {
            "type": 9,
            "data": {
                "custom_id": f"submit_edit_goal_{goal_id}",
                "title": "목표 수정",
                "components": [
                    {
                        "type": 1,
                        "components": [
                            {
                                "type": 4,
                                "custom_id": "name",
                                "label": "이름",
                                "style": 1,
                                "min_length": 1,
                                "max_length": 100,
                                "required": True,
                                "value": goal.get("name", "")
                            }
                        ]
                    },
                    {
                        "type": 1,
                        "components": [
                            {
                                "type": 4,
                                "custom_id": "category",
                                "label": "카테고리",
                                "style": 1,
                                "value": goal.get("category", "")
                            }
                        ]
                    },
                    {
                        "type": 1,
                        "components": [
                            {
                                "type": 4,
                                "custom_id": "total_goal",
                                "label": "총 목표",
                                "style": 1,
                                "value": str(goal.get("total_goal", ""))
                            }
                        ]
                    },
                    {
                        "type": 1,
                        "components": [
                            {
                                "type": 3,
                                "custom_id": "unit",
                                "options": [
                                    {"label": "개수", "value": "count"},
                                    {"label": "시간", "value": "time"},
                                    {"label": "일수", "value": "day"}
                                ],
                                "placeholder": "단위 선택",
                                "min_values": 1,
                                "max_values": 1
                            }
                        ]
                    }
                ]
            }
        }

        return JSONResponse(content=modal)
    # ✅ edit_goal → 전체 목록 조회 및 Section 응답
    elif custom_id == "edit_goal" or payload.get("data", {}).get("name") == "edit_goal":
        print("Fetching all goals for user")
        # 사용자 ID로 목표 목록 조회
        user_id = user["id"]
        response = await view_goals_api(user_id)
        if response.status_code != 200:
            return JSONResponse(content={"type": 4, "data": {"content": "❌ 목표 목록을 불러오지 못했습니다."}})
        
        goals = response.json()
        if not goals:
            return JSONResponse(content={"type": 4, "data": {"content": "등록된 목표가 없습니다."}})
        
        sections = []
        for goal in goals:
            sections.append({
                "type": 9,  # Section
                "components": [
                    {
                        "type": 1,
                        "components": [
                            {
                                "type": 2,
                                "style": 1,
                                "label": f"{goal['name']} 수정",
                                "custom_id": f"edit_goal_{goal['id']}"
                            }
                        ]
                    }
                ]
            })

        return JSONResponse(content={
            "type": 4,
            "data": {
                "content": "📋 수정할 목표를 선택하세요:",
                "components": sections,
                "flags": 1 << 15
            }
        })


async def handle_delete_goal(payload):
    custom_id = payload["data"]["custom_id"]
    goal_id = custom_id.replace("delete_goal_", "")

    await delete_goal_api(goal_id)

    return JSONResponse(content={"type": 4, "data": {"content": f"🗑️ 목표 `{goal_id}` 삭제 완료."}})


async def handle_start_goal(payload):
    custom_id = payload["data"]["custom_id"]
    goal_id = custom_id.replace("start_goal_", "")

    return JSONResponse(content={"type": 4, "data": {"content": f"🚀 목표 `{goal_id}` 학습 시작!"}})
