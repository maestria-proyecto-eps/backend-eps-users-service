from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, aliased
from db.session import get_db
from models.doctor import Doctor
from models.Persona import Persona
from models.specialty import Specialty, SpecialtyRemission
from schemas.doctor import DoctorCreate, DoctorResponse, DoctorUpdateSpecialty
from schemas.specialty import SpecialtyResponse, SpecialtyRemissionResponse
from typing import List, Optional

router = APIRouter(prefix="/api", tags=["Doctors"])

# --- SECCIÓN: MÉDICOS ---

@router.post("/doctors", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    # Verificación de la existencia de la persona en la base administrativa
    person = db.query(Persona).filter(Persona.num_documento == doctor.id_medico).first()
    if not person:
        raise HTTPException(
            status_code=404,
            detail="La persona no existe. No se puede asignar el rol de médico."
        )

    # Prevención de registros duplicados para el mismo documento
    if db.query(Doctor).filter(Doctor.id_medico == doctor.id_medico).first():
        raise HTTPException(status_code=400, detail="El usuario ya está registrado como médico.")

    # Validación de la especialidad antes de la creación
    if not db.query(Specialty).filter(Specialty.id_especialidad == doctor.id_especialidad).first():
        raise HTTPException(status_code=404, detail="Especialidad no encontrada.")

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
        raise HTTPException(status_code=500, detail=f"Error en la persistencia: {str(e)}")

@router.get("/doctors", response_model=List[DoctorResponse])

@router.get("/doctors/by-specialty/{id_especialidad}", response_model=List[DoctorResponse])
def get_doctors(
        id_especialidad: Optional[int] = None,
        num_licencia: Optional[int] = Query(None),
        db: Session = Depends(get_db)
):
    # Construcción de consulta base para la entidad médico
    query = db.query(Doctor)

    # Filtrado condicional según parámetros de búsqueda
    if id_especialidad:
        query = query.filter(Doctor.id_especialidad == id_especialidad)
    if num_licencia:
        query = query.filter(Doctor.num_licencia == num_licencia)

    return query.all()

@router.put("/doctors/{id_medico}/specialty", response_model=DoctorResponse)
def update_doctor_specialty(id_medico: int, payload: DoctorUpdateSpecialty, db: Session = Depends(get_db)):
    # Localización del médico para actualización de especialidad
    db_doctor = db.query(Doctor).filter(Doctor.id_medico == id_medico).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Médico no encontrado.")

    # Verificación de validez de la nueva especialidad
    if not db.query(Specialty).filter(Specialty.id_especialidad == payload.id_especialidad).first():
        raise HTTPException(status_code=400, detail="Especialidad inexistente.")

    db_doctor.id_especialidad = payload.id_especialidad
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

# --- SECCIÓN: ESPECIALIDADES ---

@router.get("/specialties", response_model=List[SpecialtyResponse])
def list_specialties(db: Session = Depends(get_db)):
    # Limitación del listado a las primeras 8 especialidades registradas
    return db.query(Specialty).limit(8).all()

@router.get("/specialties/remission", response_model=List[SpecialtyRemissionResponse])
def get_specialty_remissions(db: Session = Depends(get_db)):
    # Creación de alias para permitir el JOIN sobre la misma tabla (Especialidades)
    EspRemitida = aliased(Specialty)
    EspQueRemite = aliased(Specialty)

    # Consulta que cruza la tabla de asociación con la tabla de nombres
    results = db.query(
        SpecialtyRemission.id_especialidad_remitida,
        EspRemitida.nombre_especialidad.label("nombre_remitida"),
        SpecialtyRemission.id_especialidad_que_remite,
        EspQueRemite.nombre_especialidad.label("nombre_que_remite")
    ).join(
        EspRemitida,
        SpecialtyRemission.id_especialidad_remitida == EspRemitida.id_especialidad
    ).join(
        EspQueRemite,
        SpecialtyRemission.id_especialidad_que_remite == EspQueRemite.id_especialidad
    ).all()

    return results