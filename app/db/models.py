from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Enum, JSON, func, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base
import enum

class RoleEnum(enum.Enum):
    user = "user"
    admin = "admin"
    org_admin = "org_admin"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    role: Mapped[str] = mapped_column(Enum(RoleEnum), default=RoleEnum.user)
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())

class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    owner_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    branding_json: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())

class Pet(Base):
    __tablename__ = "pets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    species: Mapped[str] = mapped_column(String, default="dog")
    breed: Mapped[str] = mapped_column(String, default="unknown")
    meta_json: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())

class Story(Base):
    __tablename__ = "stories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"))
    title: Mapped[str] = mapped_column(String, default="Untitled")
    status: Mapped[str] = mapped_column(String, default="draft")
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())

class StoryRevision(Base):
    __tablename__ = "story_revisions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id: Mapped[int] = mapped_column(ForeignKey("stories.id"))
    script_text: Mapped[str] = mapped_column(String, default="")
    voice_pack_id: Mapped[int] = mapped_column(Integer, nullable=True)
    style_json: Mapped[dict] = mapped_column(JSON, default={})
    duration_sec: Mapped[int] = mapped_column(Integer, default=30)
    render_status: Mapped[str] = mapped_column(String, default="pending")
    job_id: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())

class Asset(Base):
    __tablename__ = "assets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_org_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    type: Mapped[str] = mapped_column(String) # image|audio|video
    s3_key: Mapped[str] = mapped_column(String, unique=True)
    cdn_url: Mapped[str] = mapped_column(String, nullable=True)
    duration: Mapped[int] = mapped_column(Integer, default=0)
    width: Mapped[int] = mapped_column(Integer, default=0)
    height: Mapped[int] = mapped_column(Integer, default=0)
    checksum: Mapped[str] = mapped_column(String, default="")
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())
