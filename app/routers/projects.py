from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Project
from app.schemas.schemas import ProjectOut

router = APIRouter()


@router.get("/", response_model=List[ProjectOut])
def get_projects(featured_only: bool = False, db: Session = Depends(get_db)):
    query = db.query(Project)
    if featured_only:
        query = query.filter(Project.is_featured == True)
    return query.order_by(Project.order).all()


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
