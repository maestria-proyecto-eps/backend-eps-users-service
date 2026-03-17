from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from db.session import get_db
from models.doctor import Doctor
from models.specialty import Specialty
from models.doctor import Persona
from schemas.doctor import DoctorCreate, DoctorResponse, DoctorUpdateSpecialty
from typing import List, Optional

router = APIRouter(prefix="/api/doctors", tags=["Doctors"])

# 1. CREACIÓN DE DOCTORES
@router.post("/", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def create_doctor(
        doctor: DoctorCreate,
        db: Session = Depends(get_db),
):
    # VALIDACIÓN 1: ¿Existe la persona en la DB administrativa?
    # id_medico DEBE ser un num_documento válido en la tabla PERSONA
    person_exists = db.query(Persona).filter(Persona.num_documento == doctor.id_medico).first()
    if not person_exists:
        raise HTTPException(
            status_code=404,
            detail=f"No se puede crear el médico. La persona con documento {doctor.id_medico} no existe en el sistema administrativo."
        )

    # VALIDACIÓN 2: ¿Ya es médico?
    exist_doctor = db.query(Doctor).filter(Doctor.id_medico == doctor.id_medico).first()
    if exist_doctor:
        raise HTTPException(status_code=400, detail="Este documento ya está registrado como médico")

    # VALIDACIÓN 3: ¿Existe la especialidad?
    specialty_exists = db.query(Specialty).filter(Specialty.id_especialidad == doctor.id_especialidad).first()
    if not specialty_exists:
        raise HTTPException(status_code=404, detail="La especialidad especificada no existe")

    # CREACIÓN: Solo usa los campos que existen en la tabla MEDICOS
    db_doctor = Doctor(
        id_medico=doctor.id_medico,
        num_licencia=doctor.num_licencia,
        id_especialidad=doctor.id_especialidad
    )

    try:
        db.add(db_doctor)
        db.commit()
        db.refresh(db_doctor)
        return db_doctor
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar en base de datos: {str(e)}")

# 2. LISTADO DE DOCTORES (CON FILTRO O TOTAL)
@router.get("/by-specialty/{specialty_id}", response_model=List[DoctorResponse])
def get_doctors(
        id_especialidad: Optional[int] = Query(None, description="Filtrar por ID de especialidad"),
        db: Session = Depends(get_db)
):
    """
    Obtiene la lista de doctores. Gracias al 'relationship' en el modelo,
    traerá automáticamente nombres y apellidos desde la tabla PERSONA.
    """
    query = db.query(Doctor)

    if id_especialidad is not None:
        query = query.filter(Doctor.id_especialidad == id_especialidad)

    return query.all()

# 3. CAMBIO DE ESPECIALIDAD
@router.put("/{id_medico}/specialty", response_model=DoctorResponse)
def update_doctor_specialty(
        id_medico: int,
        payload: DoctorUpdateSpecialty,
        db: Session = Depends(get_db),
):
    # 1. Buscar al doctor
    db_doctor = db.query(Doctor).filter(Doctor.id_medico == id_medico).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Médico no encontrado")

    # 2. Verificar la nueva especialidad
    specialty_exists = db.query(Specialty).filter(Specialty.id_especialidad == payload.id_especialidad).first()
    if not specialty_exists:
        raise HTTPException(
            status_code=400,
            detail="La especialidad no existe."
        )

    db_doctor.id_especialidad = payload.id_especialidad
    db.commit()
    db.refresh(db_doctor)

    return db_doctor