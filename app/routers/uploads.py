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
    if not req.key or "/" in req.key and ".." in req.key:
        raise HTTPException(status_code=400, detail="Invalid key")
    put_url = presign_put(req.key, req.content_type)
    get_url = presign_get(req.key)
    return {"put_url": put_url, "get_url": get_url}
