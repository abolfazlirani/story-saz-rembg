import io
import os
import asyncio
from typing import Optional

import aiohttp
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from rembg import remove

app = FastAPI(title="StorySaz Rembg", version="1.0.0")

REM_BG_TIMEOUT = float(os.getenv("REM_BG_TIMEOUT", "20"))

async def fetch_image(url: str) -> bytes:
    timeout = aiohttp.ClientTimeout(total=REM_BG_TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=resp.status, detail="Failed to fetch image")
            return await resp.read()

@app.get("/api/remove")
async def remove_background(url: Optional[str] = None):
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
