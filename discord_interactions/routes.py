# 파일: discord_interactions/routes.py

from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from discord_interactions.verify import verify_discord_request
from discord_interactions.handlers import (
    handle_edit_goal,
    handle_delete_goal,
    handle_start_goal
)

router = APIRouter()

@router.post("/interactions")
async def handle_interaction(request: Request, _=Depends(verify_discord_request)):
    payload = await request.json()
    interaction_type = payload.get("type")
    print(f"[INFO] Discord interaction received: type={interaction_type}")

    # 1. Discord Ping 처리 (초기 핸드셰이크용)
    if interaction_type == 1:
        print("[INFO] Ping received from Discord — responding with Pong.")
        return JSONResponse(content={"type": 1})

    # 2. 컴포넌트 인터랙션 처리 (버튼/모달 등)
    elif interaction_type == 3:
        custom_id = payload.get("data", {}).get("custom_id")
        if not custom_id:
            print("[ERROR] custom_id 없음")
            return JSONResponse(
                content={"type": 4, "data": {"content": "⚠️ custom_id가 없습니다."}},
                status_code=400
            )

        print(f"[INFO] Handling component with custom_id: {custom_id}")

        if custom_id.startswith("edit_goal"):
            return await handle_edit_goal(payload)
        elif custom_id.startswith("delete_goal"):
            return await handle_delete_goal(payload)
        elif custom_id.startswith("start_goal"):
            return await handle_start_goal(payload)
        else:
            return JSONResponse(
                content={"type": 4, "data": {"content": f"알 수 없는 custom_id: {custom_id}"}},
                status_code=400
            )

    # 3. Slash Command 전송에 대해 가능한 프로퍼 응답
    elif interaction_type == 2:
        command_name = payload.get("data", {}).get("name")
        print(f"[INFO] Slash command received: {command_name}")
        return JSONResponse(content={
            "type": 4,
            "data": {
                "content": f"명령어 '{command_name}'를 받았습니다."
            }
        })

    # 4. 지원되지 않는 유형
    else:
        print(f"[ERROR] Unknown interaction type: {interaction_type}")
        return JSONResponse(
            content={"type": 4, "data": {"content": "⚠️ 지원되지 않는 interaction type입니다."}},
            status_code=400
        )
