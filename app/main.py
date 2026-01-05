import io
import os
import asyncio
from typing import Optional

import aiohttp
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from rembg import remove

app = FastAPI(title="StorySaz Rembg", version="1.0.0")

REM_BG_TIMEOUT = float(os.getenv("REM_BG_TIMEOUT", "20"))
REMBG_API_TOKEN = os.getenv("REMBG_API_TOKEN")

def verify_token(request: Request):
    """Verify API token from request headers."""
    token = request.headers.get("X-API-Token")
    if not token:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
    
    if not REMBG_API_TOKEN:
        raise HTTPException(status_code=500, detail="API token not configured")
    
    if token != REMBG_API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

async def fetch_image(url: str) -> bytes:
    timeout = aiohttp.ClientTimeout(total=REM_BG_TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=resp.status, detail="Failed to fetch image")
            return await resp.read()

@app.get("/api/remove")
async def remove_background(request: Request, url: Optional[str] = None):
    verify_token(request)
    if not url:
        raise HTTPException(status_code=400, detail="url is required")
    try:
        original = await fetch_image(url)
        loop = asyncio.get_event_loop()
        processed: bytes = await loop.run_in_executor(None, remove, original)
        if not processed:
            raise HTTPException(status_code=500, detail="Failed to process image")
        return Response(content=processed, media_type="image/png")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {e}")
