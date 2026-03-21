from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


# ── PROJECT ──────────────────────────────────────────────
class ProjectBase(BaseModel):
    num: str
    title: str
    org: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None
    stack: List[str] = []
    color: str = "#f97316"
    live_url: Optional[str] = None
    github_url: Optional[str] = None
    is_featured: bool = True
    order: int = 0


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    num: Optional[str] = None
    title: Optional[str] = None
    org: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None
    stack: Optional[List[str]] = None
    color: Optional[str] = None
    live_url: Optional[str] = None
    github_url: Optional[str] = None
    is_featured: Optional[bool] = None
    order: Optional[int] = None


class ProjectOut(ProjectBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── SKILL GROUP ───────────────────────────────────────────
class SkillGroupBase(BaseModel):
    group: str
    color: str = "#f97316"
    tags: List[str] = []
    order: int = 0


class SkillGroupCreate(SkillGroupBase):
    pass


class SkillGroupUpdate(BaseModel):
    group: Optional[str] = None
    color: Optional[str] = None
    tags: Optional[List[str]] = None
    order: Optional[int] = None


class SkillGroupOut(SkillGroupBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── CERTIFICATION ─────────────────────────────────────────
class CertificationBase(BaseModel):
    name: str
    org: Optional[str] = None
    date: Optional[str] = None
    credential_url: Optional[str] = None
    order: int = 0


class CertificationCreate(CertificationBase):
    pass


class CertificationUpdate(BaseModel):
    name: Optional[str] = None
    org: Optional[str] = None
    date: Optional[str] = None
    credential_url: Optional[str] = None
    order: Optional[int] = None


class CertificationOut(CertificationBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── CONTACT ───────────────────────────────────────────────
class ContactCreate(BaseModel):
    name: str
    email: str
    subject: Optional[str] = None
    message: str


class ContactOut(ContactCreate):
    id: int
    is_read: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── AUTH ──────────────────────────────────────────────────
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
