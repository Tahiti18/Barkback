# BarkBacks Backend (FastAPI + Celery)

Single-command local run:
```
cp .env.example .env
docker compose up --build
```
Then:
- API: http://localhost:8000/health
- Celery worker + beat run automatically.
- Alembic: `docker compose exec api alembic upgrade head`

Next step (after scaffold): wire DB models into routes, add S3 buckets, and integrate real render pipeline.
