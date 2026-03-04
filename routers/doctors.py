from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from db.session import get_db
from models.Usuario import Usuario
from models.doctor import Doctor
from models.specialty import Specialty
from schemas.doctor import DoctorCreate, DoctorResponse, DoctorUpdateSpecialty


router = APIRouter(prefix="/api/doctors", tags=["Doctors"])


@router.post("/", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    if db.query(Doctor).filter(Doctor.id_medico == doctor.id_medico).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El ID de medico ya esta registrado")

    if db.query(Doctor).filter(Doctor.num_licencia == doctor.num_licencia).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El numero de licencia ya esta registrado")

    if db.query(Doctor).filter(Doctor.id_usuario == doctor.id_usuario).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario ya tiene un medico asociado")

    if not db.query(Usuario).filter(Usuario.id_usuario == doctor.id_usuario).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no existe")

    if not db.query(Specialty).filter(Specialty.id_especialidad == doctor.id_especialidad).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La especialidad con ID {doctor.id_especialidad} no existe. Por favor verifique el catalogo.",
        )

    db_doctor = Doctor(**doctor.model_dump())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


@router.get("/by-specialty/", response_model=List[DoctorResponse])
def get_doctors_by_specialty(
    id_especialidad: Optional[int] = Query(None, description="Filtrar doctores por el ID de su especialidad"),
    db: Session = Depends(get_db),
):
    query = db.query(Doctor)
    if id_especialidad is not None:
        query = query.filter(Doctor.id_especialidad == id_especialidad)
    return query.order_by(Doctor.id_medico).all()


@router.put("/{id_medico}/specialty", response_model=DoctorResponse)
def update_doctor_specialty(
    id_medico: int,
    payload: DoctorUpdateSpecialty,
    db: Session = Depends(get_db),
):
    db_doctor = db.query(Doctor).filter(Doctor.id_medico == id_medico).first()
    if not db_doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medico no encontrado")

    specialty_exists = db.query(Specialty).filter(Specialty.id_especialidad == payload.id_especialidad).first()
    if not specialty_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La especialidad con ID {payload.id_especialidad} no existe. Por favor verifique el catalogo.",
        )

    db_doctor.id_especialidad = payload.id_especialidad
    db.commit()
    db.refresh(db_doctor)
    return db_doctor
