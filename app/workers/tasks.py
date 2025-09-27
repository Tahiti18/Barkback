from app.workers.celery_app import celery_app
import time, logging

logger = logging.getLogger(__name__)

@celery_app.task(name="render.story")
def render_story(job_payload: dict):
    logger.info("Started render job: %s", job_payload)
    # TEMPORARY: simulate render work with sleep; integrate FFmpeg + models in next step.
    time.sleep(3)
    # Return a pretend asset key to be looked up or generated.
    return {"status": "done", "asset_s3_key": job_payload.get("output_key", "videos/final.mp4")}
