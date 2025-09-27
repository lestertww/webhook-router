# app/router_engine.py

import asyncio
import httpx
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Router, Rule, Event

# ----------------------
# Rule Evaluation Helper
# ----------------------
def evaluate_condition(condition: Dict[str, Any], payload: Dict[str, Any]) -> bool:
    """
    Evaluate a single JSON condition against the payload.
    Example condition:
    {
        "field": "event.type",
        "operator": "equals",
        "value": "payment.succeeded"
    }
    """
    try:
        # Support nested fields like "event.type"
        field_path = condition["field"].split(".")
        value = payload
        for key in field_path:
            value = value.get(key, None)
        operator = condition.get("operator", "equals")
        expected = condition.get("value")

        if operator == "equals":
            return value == expected
        elif operator == "not_equals":
            return value != expected
        elif operator == "greater_than":
            return value > expected
        elif operator == "less_than":
            return value < expected
        # Add more operators as needed
        return False
    except Exception:
        return False

# ----------------------
# Forward Payload Async
# ----------------------
async def forward_payload(urls: List[str], payload: Dict[str, Any], headers: Dict[str, Any]):
    async def send(url):
        async with httpx.AsyncClient() as client:
            try:
                await client.post(url, json=payload, headers=headers, timeout=10.0)
            except Exception as e:
                print(f"Failed to forward to {url}: {e}")

    await asyncio.gather(*(send(url) for url in urls))

# ----------------------
# Main Webhook Handler
# ----------------------
async def handle_webhook(router_id: str, payload: Dict[str, Any], headers: Dict[str, Any]) -> List[str]:
    """
    Handles an incoming webhook:
    - Fetch router and rules from DB
    - Evaluate rules
    - Forward to target URLs
    - Log event
    """
    forwarded_urls = []
    rules_fired = []

    # Open DB session
    db: Session = SessionLocal()

    try:
        router = db.query(Router).filter(Router.id == router_id).first()
        if not router:
            raise Exception(f"Router {router_id} not found")

        # Evaluate all rules
        for rule in router.rules:
            condition_json = rule.condition_json
            if evaluate_condition(condition_json, payload):
                await forward_payload(rule.target_urls, payload, headers)
                forwarded_urls.extend(rule.target_urls)
                rules_fired.append(rule.id)

        # Log the event
        event = Event(
            router_id=router.id,
            raw_payload=payload,
            headers=headers,
            rules_fired=rules_fired,
            forwarded_to=forwarded_urls,
            signature_valid=None  # Implement later if needed
        )
        db.add(event)
        db.commit()

    finally:
        db.close()

    return forwarded_urls
