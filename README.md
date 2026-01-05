# StorySaz Rembg Service

FastAPI/uvicorn wrapper around `rembg` with a simple GET endpoint compatible with the existing Node worker (`/api/remove?url=...`).

## Endpoints
- `GET /api/remove?url=<image_url>` -> returns PNG with background removed (binary body)

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Test:
```bash
curl -L "http://localhost:8000/api/remove?url=https://example.com/image.png" --output out.png
```

## Docker
```bash
docker build -t story-saz-rembg .
docker run -p 8000:8000 --env-file .env story-saz-rembg
```

## Config
See `.env.example` for tunables:
- `REM_BG_TIMEOUT` (seconds): HTTP timeout when fetching the source image.
