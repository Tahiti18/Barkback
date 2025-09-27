from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.deps.auth import get_current_user
from app.services.s3 import presign_put, presign_get

router = APIRouter(prefix="/v1/uploads", tags=["uploads"])

class PresignRequest(BaseModel):
    key: str
    content_type: str

@router.post("/presign")
def presign(req: PresignRequest, user=Depends(get_current_user)):
    if not req.key or (".." in req.key):
        raise HTTPException(status_code=400, detail="Invalid key")
    put_url = presign_put(req.key, req.content_type)
    get_url = presign_get(req.key)
    return {"put_url": put_url, "get_url": get_url}

# --- Temporary GET route for quick testing on iPad ---
@router.get("/presign/test")
def presign_test(user=Depends(get_current_user)):
    key = "dev/test.txt"
    ct = "text/plain"
    put_url = presign_put(key, ct)
    get_url = presign_get(key)
    return {"key": key, "content_type": ct, "put_url": put_url, "get_url": get_url}
