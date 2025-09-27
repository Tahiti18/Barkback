from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from app.config import settings
from app.utils.logging import configure_logging
from app.routers import uploads, stories, billing

configure_logging()

app = FastAPI(title="BarkBacks API", default_response_class=ORJSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins or ["*"] if settings.env == "development" else settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(uploads.router)
app.include_router(stories.router)
app.include_router(billing.router)
