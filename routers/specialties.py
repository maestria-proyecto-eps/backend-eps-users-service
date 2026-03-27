from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from models.specialty import Specialty
from schemas.specialty import SpecialtyResponse

router = APIRouter(
    prefix="/api/specialties",
    tags=["Specialties"]
)

# OBTENER TODAS LAS ESPECIALIDADES PRESENTES EN LA EPS
@router.get("/", response_model=List[SpecialtyResponse])
def get_specialties(db: Session = Depends(get_db)):
    specialties = db.query(Specialty).limit(8).all()
    return specialties

