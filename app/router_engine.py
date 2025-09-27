# app/router_engine.py

import asyncio
import httpx
from typing import List

# Placeholder for database lookup (to be implemented)
# Example structure:
# routers_db = {
#     "abcd1234": {
#         "rules": [
#             {"condition": lambda payload: payload.get("event") == "payment.succeeded",
#              "target_urls": ["https://example.com/callback1"]}
#         ]
#     }
# }

async def handle_webhook(router_id: str, payload: dict, headers: dict) -> List[str]:
    """
    Handles an incoming webhook:
    - Evaluates rules
    - Forwards payload to target URLs
    - Returns list of URLs forwarded to
    """
    # TODO: Fetch router metadata & rules from DB
    router = get_router_stub(router_id)
    if not router:
        raise Exception(f"Router {router_id} not found")

    forwarded_urls = []

    # Evaluate rules (stub logic)
    for rule in router["rules"]:
        if evaluate_rule(rule["condition"], payload):
            # Forward payload to each target URL asynchronously
            await forward_payload(rule["target_urls"], payload, headers)
            forwarded_urls.extend(rule["target_urls"])

    return forwarded_urls

# ----------------------
# Helper functions
# ----------------------

def get_router_stub(router_id: str) -> dict:
    """
    Stub function to simulate router + rules from DB.
    Replace with real DB query.
    """
    if router_id == "test1234":
        return {
            "rules": [
                {
                    "condition": lambda payload: payload.get("event") == "payment.succeeded",
                    "target_urls": ["https://webhook.site/xxxx"]
                }
            ]
        }
    return None

def evaluate_rule(condition, payload: dict) -> bool:
    """
    Evaluate the condition function for the payload.
    """
    try:
        return condition(payload)
    except Exception:
        return False

async def forward_payload(urls: list, payload: dict, headers: dict):
    """
    Forward payload asynchronously to all target URLs.
    """
    async def send(url):
        async with httpx.AsyncClient() as client:
            try:
                await client.post(url, json=payload, headers=headers, timeout=10.0)
            except Exception as e:
                print(f"Failed to forward to {url}: {e}")

    # Run all forwards concurrently
    await asyncio.gather(*(send(url) for url in urls))

