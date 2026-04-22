from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from models.specialty import Specialty
from schemas.specialty import SpecialtyResponse
# Importamos las dependencias de seguridad
from core.dependencias import RequireRole

router = APIRouter(
    prefix="/api/specialties",
    tags=["Specialties"]
)

# Protegido: Permitimos acceso a médicos, talento humano y pacientes
@router.get("/", response_model=List[SpecialtyResponse])
def get_specialties(
        db: Session = Depends(get_db),
        current_user: dict = Depends(RequireRole(["Talento Humano", "Médico", "Paciente"]))
):
    specialties = db.query(Specialty).limit(8).all()
    return specialties