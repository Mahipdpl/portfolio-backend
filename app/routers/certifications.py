from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Certification
from app.schemas.schemas import CertificationOut

router = APIRouter()


@router.get("/", response_model=List[CertificationOut])
def get_certifications(db: Session = Depends(get_db)):
    return db.query(Certification).order_by(Certification.order).all()
