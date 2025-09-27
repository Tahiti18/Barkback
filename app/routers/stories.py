from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.deps.auth import get_current_user
from app.workers.tasks import render_story

router = APIRouter(prefix="/v1/stories", tags=["stories"])

class CreateStory(BaseModel):
    pet_id: int
    title: str = "Untitled"

class RenderRequest(BaseModel):
    story_id: int
    revision_id: int | None = None
    output_key: str = "videos/story.mp4"

@router.post("")
def create_story(payload: CreateStory, user=Depends(get_current_user)):
    # In step 2, persist to DB; here return a stub response with deterministic id for front-end wiring.
    return {"id": 1, "title": payload.title, "pet_id": payload.pet_id, "status": "draft"}

@router.post("/render")
def render(payload: RenderRequest, user=Depends(get_current_user)):
    job = render_story.delay(payload.model_dump())
    return {"job_id": job.id, "status": "queued"}

@router.get("/jobs/{job_id}")
def job_status(job_id: str):
    async_result = render_story.AsyncResult(job_id)
    if async_result.successful():
        return {"status": "done", "result": async_result.result}
    if async_result.failed():
        return {"status": "failed"}
    return {"status": async_result.status.lower()}
