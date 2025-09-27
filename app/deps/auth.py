from fastapi import Header, HTTPException
import httpx, time
from functools import lru_cache
from app.config import settings
from jose import jwk, jwt
from jose.utils import base64url_decode

# ---------- DEV BYPASS (for non-production only) ----------
def _dev_bypass(authorization: str | None):
    # Allows "Authorization: Bearer dev" when ENV is not production
    if settings.env != "production" and authorization:
        parts = authorization.split(" ", 1)
        if len(parts) == 2 and parts[0].lower() == "bearer" and parts[1] == "dev":
            return {"sub": "dev-user", "email": "dev@example.com", "org_id": 1}
    return None
# ----------------------------------------------------------

@lru_cache(maxsize=1)
def get_jwks():
    if not settings.clerk_jwks_url:
        raise HTTPException(status_code=500, detail="JWKS URL not configured")
    with httpx.Client(timeout=5) as c:
        resp = c.get(settings.clerk_jwks_url)
        resp.raise_for_status()
        return resp.json()

def verify_jwt(token: str):
    headers = jwt.get_unverified_header(token)
    kid = headers.get("kid")
    jwks = get_jwks()
    key = next((k for k in jwks["keys"] if k["kid"] == kid), None)
    if not key:
        raise HTTPException(status_code=401, detail="Unknown key")
    message, encoded_sig = token.rsplit(".", 1)
    decoded_sig = base64url_decode(encoded_sig.encode())
    public_key = jwk.construct(key)
    if not public_key.verify(message.encode(), decoded_sig):
        raise HTTPException(status_code=401, detail="Bad signature")
    claims = jwt.get_unverified_claims(token)
    now = int(time.time())
    if claims.get("iss") != settings.clerk_issuer:
        raise HTTPException(status_code=401, detail="Bad issuer")
    if settings.clerk_audience and claims.get("aud") != settings.clerk_audience:
        raise HTTPException(status_code=401, detail="Bad audience")
    if now > int(claims.get("exp", 0)):
        raise HTTPException(status_code=401, detail="Token expired")
    return claims

def get_current_user(authorization: str | None = Header(None)):
    # Allow simple "Bearer dev" when not in production
    dev_user = _dev_bypass(authorization)
    if dev_user:
        return dev_user

    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.split(" ", 1)[1]
    claims = verify_jwt(token)
    return {"sub": claims.get("sub"), "email": claims.get("email"), "org_id": claims.get("org_id")}
