from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db_audit
from models.specialty import Specialty
from schemas.specialty import SpecialtyResponse
from core.dependencias import get_usuario_actual
router = APIRouter(
    prefix="/api/specialties",
    tags=["Specialties"]
)

# OBTENER TODAS LAS ESPECIALIDADES PRESENTES EN LA EPS
@router.get("/", response_model=List[SpecialtyResponse], dependencies=[Depends(get_usuario_actual)])
def get_specialties(db: Session = Depends(get_db_audit)):
    specialties = db.query(Specialty).limit(8).all()
    return specialties

