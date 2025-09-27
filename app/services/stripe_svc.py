import stripe
from app.config import settings

stripe.api_key = settings.stripe_api_key

def create_billing_portal(customer_id: str):
    return stripe.billing_portal.Session.create(customer=customer_id)

def verify_webhook(sig_header: str, payload: bytes):
    return stripe.Webhook.construct_event(
        payload=payload,
        sig_header=sig_header,
        secret=settings.stripe_webhook_secret,
    )
