from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import SkillGroup
from app.schemas.schemas import SkillGroupOut

router = APIRouter()


@router.get("/", response_model=List[SkillGroupOut])
def get_skills(db: Session = Depends(get_db)):
    return db.query(SkillGroup).order_by(SkillGroup.order).all()
