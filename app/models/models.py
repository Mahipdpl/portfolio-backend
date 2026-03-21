from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    num = Column(String(10), nullable=False)
    title = Column(String(200), nullable=False)
    org = Column(String(200))
    date = Column(String(50))
    description = Column(Text)
    stack = Column(JSON, default=list)   # stored as JSON array
    color = Column(String(20), default="#f97316")
    live_url = Column(String(300), nullable=True)
    github_url = Column(String(300), nullable=True)
    is_featured = Column(Boolean, default=True)
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SkillGroup(Base):
    __tablename__ = "skill_groups"

    id = Column(Integer, primary_key=True, index=True)
    group = Column(String(100), nullable=False)
    color = Column(String(20), default="#f97316")
    tags = Column(JSON, default=list)
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    org = Column(String(200))
    date = Column(String(50))
    credential_url = Column(String(300), nullable=True)
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    subject = Column(String(300))
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(300), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
