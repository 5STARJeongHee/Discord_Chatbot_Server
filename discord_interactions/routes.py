# api_server/discord_interactions/routes.py
from fastapi import APIRouter, Request, Header, HTTPException
from fastapi.responses import JSONResponse
from discord_interactions.handlers import handle_edit_goal, handle_delete_goal, handle_start_goal
import nacl.signing
import nacl.exceptions
import os

router = APIRouter()

DISCORD_PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")

@router.post("/interactions")
async def handle_interaction(
    request: Request,
    x_signature_ed25519: str = Header(...),
    x_signature_timestamp: str = Header(...)
):
    body = await request.body()

    # 🔐 인증 절차
    verify_key = nacl.signing.VerifyKey(bytes.fromhex(DISCORD_PUBLIC_KEY))
    try:
        verify_key.verify(
            f"{x_signature_timestamp.decode() if isinstance(x_signature_timestamp, bytes) else x_signature_timestamp}{body.decode()}".encode(),
            bytes.fromhex(x_signature_ed25519)
        )
    except nacl.exceptions.BadSignatureError:
        raise HTTPException(status_code=401, detail="Invalid request signature")

    # 🔄 JSON 파싱 및 처리
    payload = await request.json()
    custom_id = payload.get("data", {}).get("custom_id")

    if custom_id is None:
        return JSONResponse(content={"error": "No custom_id provided."}, status_code=400)

    if custom_id.startswith("edit_goal"):
        return await handle_edit_goal(payload)
    elif custom_id.startswith("delete_goal"):
        return await handle_delete_goal(payload)
    elif custom_id.startswith("start_goal"):
        return await handle_start_goal(payload)
    else:
        return JSONResponse(content={"error": "Unknown custom_id."}, status_code=400)
