from fastapi import Request, HTTPException
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from config.properties import DISCORD_PUBLIC_KEY

if not DISCORD_PUBLIC_KEY:
    raise RuntimeError("DISCORD_PUBLIC_KEY not found in environment")

verify_key = VerifyKey(bytes.fromhex(DISCORD_PUBLIC_KEY))

async def verify_discord_request(request: Request):
    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")

    if not signature or not timestamp:
        raise HTTPException(status_code=401, detail="Missing signature headers")

    body = (await request.body()).decode("utf-8")

    try:
        verify_key.verify(f"{timestamp}{body}".encode(), bytes.fromhex(signature))
    except BadSignatureError:
        raise HTTPException(status_code=401, detail="Invalid request signature")
