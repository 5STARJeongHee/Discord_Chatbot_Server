from fastapi import APIRouter, Request, Depends
from discord_interactions.verify import verify_discord_request
from fastapi.responses import JSONResponse

from discord_interactions.handlers.slash_command_handlers import handle_slash_command
from discord_interactions.handlers.component_handlers import handle_component
from discord_interactions.handlers.modal_handlers import handle_modal

router = APIRouter()

@router.post("/interactions")
async def interactions(request: Request, _=Depends(verify_discord_request)):
    print(Request)
    payload = await request.json()
    interaction_type = payload.get("type")

    # 1. PING
    if interaction_type == 1:
        return {"type": 1}

    # 2. Slash Command
    elif interaction_type == 2:
        return await handle_slash_command(payload)

    # 3. Component (Button, Select Menu)
    elif interaction_type == 3:
        return await handle_component(payload)

    # 4. Modal Submit
    elif interaction_type == 5:
        return await handle_modal(payload)

    return JSONResponse(
        status_code=400,
        content={"type": 4, "data": {"content": "⚠️ 지원되지 않는 interaction type입니다."}}
    )
