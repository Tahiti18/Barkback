from pydantic import BaseModel, Field
from pydantic import field_validator
import os, json

class Settings(BaseModel):
    env: str = Field(default=os.getenv("ENV", "development"))
    port: int = Field(default=int(os.getenv("PORT", "8000")))
    database_url: str = Field(default=os.getenv("DATABASE_URL", ""))
    redis_url: str = Field(default=os.getenv("REDIS_URL", ""))

    aws_region: str = Field(default=os.getenv("AWS_REGION", ""))
    aws_s3_bucket: str = Field(default=os.getenv("AWS_S3_BUCKET", ""))
    aws_access_key_id: str = Field(default=os.getenv("AWS_ACCESS_KEY_ID", ""))
    aws_secret_access_key: str = Field(default=os.getenv("AWS_SECRET_ACCESS_KEY", ""))

    stripe_api_key: str = Field(default=os.getenv("STRIPE_API_KEY", ""))
    stripe_webhook_secret: str = Field(default=os.getenv("STRIPE_WEBHOOK_SECRET", ""))

    clerk_jwks_url: str = Field(default=os.getenv("CLERK_JWKS_URL", ""))
    clerk_issuer: str = Field(default=os.getenv("CLERK_ISSUER", ""))
    clerk_audience: str = Field(default=os.getenv("CLERK_AUDIENCE", ""))

    sentry_dsn: str = Field(default=os.getenv("SENTRY_DSN", ""))

    cors_origins: list[str] = Field(default_factory=list)

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors(cls, v):
        if isinstance(v, list):
            return v
        if not v:
            return []
        try:
            return json.loads(v)
        except Exception:
            return [s.strip() for s in v.split(",")]

settings = Settings()
