import os
from celery import Celery
from app.config import settings

celery_app = Celery(
    "barkbacks",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    broker_transport_options={"visibility_timeout": 3600},
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)
