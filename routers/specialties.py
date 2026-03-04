from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from models.specialty import Specialty
from schemas.specialty import SpecialtyResponse


router = APIRouter(prefix="/api/specialties", tags=["Specialties"])


@router.get("/", response_model=List[SpecialtyResponse])
def get_specialties(db: Session = Depends(get_db)):
    return db.query(Specialty).order_by(Specialty.id_especialidad).all()
