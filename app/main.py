# app/main.py

from fastapi import FastAPI, Request
from app.router_engine import handle_webhook

app = FastAPI(title="Webhook Router MVP", version="0.1")

@app.get("/")
async def root():
    return {"message": "Webhook Router is running!"}

@app.post("/hook/{router_id}")
async def webhook(router_id: str, request: Request):
    """
    Dynamic inbound webhook endpoint.
    Receives any webhook sent to /hook/{router_id}.
    """
    try:
        payload = await request.json()
    except Exception:
        return {"status": "error", "message": "Invalid JSON payload"}

    headers = dict(request.headers)

    # Handle routing, logging, forwarding
    try:
        forwarded_urls = await handle_webhook(router_id, payload, headers)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {
        "status": "received",
        "router_id": router_id,
        "forwarded_to": forwarded_urls
    }
