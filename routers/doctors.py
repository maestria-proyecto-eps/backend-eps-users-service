from fastapi import APIRouter, Depends, HTTPException, Query, Header, status
from sqlalchemy.orm import Session
from db.session import get_db
from models.doctor import Doctor
from schemas.doctor import DoctorCreate, DoctorResponse, DoctorUpdateSpecialty
from typing import List
from typing import Optional

router = APIRouter(prefix="/api/doctors", tags=["Doctors"])

# SOLO HR
def verify_hr_role(role: str = Header(..., description="El rol del usuario que hace la petición")):
    if role.lower() != "hr": # Se realizó un if para poder realizar pruebas en swagger, se espera generar tokens
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: Solo el personal de HR puede realizar esta acción"
        )
    return role

# CREACIÓN DE DOCTORES (UNICAMENTE HR)
@router.post("/", response_model=DoctorResponse)
def create_doctor(
        doctor: DoctorCreate,
        db: Session = Depends(get_db),
):
    db_doctor = Doctor(
        nombres=doctor.nombres,
        apellidos=doctor.apellidos,
        num_licencia=doctor.num_licencia,
        id_especialidad=doctor.id_especialidad,
        id_usuario=doctor.id_usuario,
        estado=doctor.estado
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

# REQUEST DE DOCTOR SEGÚN SU ESPECIALIDAD
@router.get("/by-specialty/", response_model=List[DoctorResponse])
def get_doctors_by_specialty(
        id_especialidad: Optional[int] = Query(None, description="Filtrar doctores por el ID de su especialidad"),
        db: Session = Depends(get_db)
):
    """
        ### Obtiene la lista de doctores.
        Permite visualizar todos los médicos registrados o filtrar por una especialidad específica.

        **Guía rápida de IDs de especialidades:**
        * **1**: Medicina General
        * **2**: Pediatría
        * **3**: Cardiología
        * **4**: Ginecología
        * **5**: Dermatología
        * **6**: Neurología
        * **7**: Psiquiatría
        * **8**: Ortopedia

        *Si no se proporciona un ID, el sistema devolverá el listado completo.*
        """

    query = db.query(Doctor)

    if id_especialidad is not None:
        query = query.filter(Doctor.id_especialidad == id_especialidad)

    return query.all() # Devolverá todos los MEDICOS si no se da una id de especialidad

# CAMBIO DE ESPECIALIDAD DENTRO DE LA EPS PARA EL MEDICO (SOLO HR)
@router.put("/{id_medico}/specialty", response_model=DoctorResponse)
def update_doctor_specialty(
        id_medico: int,
        payload: DoctorUpdateSpecialty,
        db: Session = Depends(get_db),
):
    """
    ### Asigna o cambia la especialidad de un médico.
    Recibe el ID del médico en la URL y el nuevo ID de especialidad en el cuerpo (JSON).
    """
    # 1. Buscar al doctor por su ID
    db_doctor = db.query(Doctor).filter(Doctor.id_medico == id_medico).first()

    # 2. Si no existe, lanzar error 404
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Médico no encontrado")

    # 3. Actualizar solo el campo de especialidad
    db_doctor.id_especialidad = payload.id_especialidad

    # 4. Guardar cambios en PostgreSQL
    db.commit()
    db.refresh(db_doctor)

    return db_doctor
