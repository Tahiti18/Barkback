from fastapi import APIRouter, Request, Header, HTTPException
from app.services.stripe_svc import create_billing_portal, verify_webhook

router = APIRouter(prefix="/v1/billing", tags=["billing"])

@router.post("/portal")
def portal(customer_id: str):
    session = create_billing_portal(customer_id)
    return {"url": session.url}

@router.post("/webhook")
async def webhook(request: Request, stripe_signature: str = Header(None, alias="Stripe-Signature")):
    payload = await request.body()
    try:
        event = verify_webhook(stripe_signature, payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # TODO: enqueue entitlement sync by event type
    return {"received": True, "type": event["type"]}
