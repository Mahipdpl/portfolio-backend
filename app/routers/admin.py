from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Project, SkillGroup, Certification, ContactMessage, AdminUser
from app.schemas.schemas import (
    ProjectCreate, ProjectUpdate, ProjectOut,
    SkillGroupCreate, SkillGroupUpdate, SkillGroupOut,
    CertificationCreate, CertificationUpdate, CertificationOut,
    ContactOut,
)
from app.core.security import get_current_admin, hash_password

router = APIRouter()

# ── PROJECTS ──────────────────────────────────────────────────────────────────

@router.get("/projects", response_model=List[ProjectOut])
def admin_list_projects(db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return db.query(Project).order_by(Project.order).all()


@router.post("/projects", response_model=ProjectOut, status_code=201)
def admin_create_project(payload: ProjectCreate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.put("/projects/{project_id}", response_model=ProjectOut)
def admin_update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project


@router.delete("/projects/{project_id}", status_code=204)
def admin_delete_project(project_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()


# ── SKILLS ────────────────────────────────────────────────────────────────────

@router.get("/skills", response_model=List[SkillGroupOut])
def admin_list_skills(db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return db.query(SkillGroup).order_by(SkillGroup.order).all()


@router.post("/skills", response_model=SkillGroupOut, status_code=201)
def admin_create_skill(payload: SkillGroupCreate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    skill = SkillGroup(**payload.model_dump())
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


@router.put("/skills/{skill_id}", response_model=SkillGroupOut)
def admin_update_skill(skill_id: int, payload: SkillGroupUpdate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    skill = db.query(SkillGroup).filter(SkillGroup.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill group not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(skill, field, value)
    db.commit()
    db.refresh(skill)
    return skill


@router.delete("/skills/{skill_id}", status_code=204)
def admin_delete_skill(skill_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    skill = db.query(SkillGroup).filter(SkillGroup.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill group not found")
    db.delete(skill)
    db.commit()


# ── CERTIFICATIONS ────────────────────────────────────────────────────────────

@router.get("/certifications", response_model=List[CertificationOut])
def admin_list_certs(db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return db.query(Certification).order_by(Certification.order).all()


@router.post("/certifications", response_model=CertificationOut, status_code=201)
def admin_create_cert(payload: CertificationCreate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    cert = Certification(**payload.model_dump())
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert


@router.put("/certifications/{cert_id}", response_model=CertificationOut)
def admin_update_cert(cert_id: int, payload: CertificationUpdate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    cert = db.query(Certification).filter(Certification.id == cert_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(cert, field, value)
    db.commit()
    db.refresh(cert)
    return cert


@router.delete("/certifications/{cert_id}", status_code=204)
def admin_delete_cert(cert_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    cert = db.query(Certification).filter(Certification.id == cert_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")
    db.delete(cert)
    db.commit()


# ── CONTACT MESSAGES ──────────────────────────────────────────────────────────

@router.get("/messages", response_model=List[ContactOut])
def admin_list_messages(unread_only: bool = False, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    query = db.query(ContactMessage)
    if unread_only:
        query = query.filter(ContactMessage.is_read == False)
    return query.order_by(ContactMessage.created_at.desc()).all()


@router.patch("/messages/{msg_id}/read", response_model=ContactOut)
def admin_mark_read(msg_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    msg = db.query(ContactMessage).filter(ContactMessage.id == msg_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    msg.is_read = True
    db.commit()
    db.refresh(msg)
    return msg


@router.delete("/messages/{msg_id}", status_code=204)
def admin_delete_message(msg_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    msg = db.query(ContactMessage).filter(ContactMessage.id == msg_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(msg)
    db.commit()


# ── CHANGE PASSWORD ───────────────────────────────────────────────────────────

@router.post("/change-password")
def change_password(
    old_password: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    from app.core.security import verify_password
    if not verify_password(old_password, current_admin.hashed_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    current_admin.hashed_password = hash_password(new_password)
    db.commit()
    return {"message": "Password updated successfully"}
