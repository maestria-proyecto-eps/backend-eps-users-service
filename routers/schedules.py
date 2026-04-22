from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db, get_db_operative
from models.schedule import Agenda
from models.doctor import Doctor
from schemas.schedule import ScheduleCreate, ScheduleResponse, TimeSlot
from typing import List, Optional
from datetime import datetime, timedelta, date
from core.dependencias import RequireRole

router = APIRouter(prefix="/api/schedules", tags=["Schedules"])

# --- CREAR AGENDA (POST) ---
@router.post("/", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_schedule(
        schedule: ScheduleCreate,
        db_admin: Session = Depends(get_db),
        db_oper: Session = Depends(get_db_operative),
        current_user: dict = Depends(RequireRole(["Talento Humano", "Médico"]))
):
    """
    Crea un bloque de agenda.
    Valida la existencia del médico en la DB Administrativa y solapamientos en la Operativa.
    """
    # 1. Validación de existencia del médico en la DB Administrativa
    doctor_exists = db_admin.query(Doctor).filter(Doctor.id_medico == schedule.id_doctor).first()
    if not doctor_exists:
        raise HTTPException(
            status_code=404,
            detail="El médico no existe en la base de datos administrativa"
        )

    # 2. Búsqueda de solapamientos en la DB Operativa
    overlap = db_oper.query(Agenda).filter(
        Agenda.id_doctor == schedule.id_doctor,
        Agenda.fecha == schedule.fecha,
        Agenda.estado == 1,
        Agenda.hora_inicio < schedule.hora_fin,
        Agenda.hora_fin > schedule.hora_inicio
    ).first()

    if overlap:
        raise HTTPException(
            status_code=400,
            detail=f"Conflicto: Ya existe un bloque para este médico el {schedule.fecha} ({overlap.hora_inicio} - {overlap.hora_fin})"
        )

    # 3. Creación en la DB Operativa
    db_agenda = Agenda(**schedule.model_dump())
    db_oper.add(db_agenda)
    db_oper.commit()
    db_oper.refresh(db_agenda)
    return db_agenda


# --- OBTENER AGENDAS (GET) ---
@router.get("/", response_model=List[ScheduleResponse])
def get_schedules(
        id_agenda: Optional[int] = None,
        db_oper: Session = Depends(get_db_operative),
        current_user: dict = Depends(RequireRole(["Talento Humano", "Médico", "Paciente"]))
):
    query = db_oper.query(Agenda)

    if id_agenda:
        item = query.filter(Agenda.id_agenda == id_agenda).first()
        if not item:
            raise HTTPException(status_code=404, detail="Registro de agenda no encontrado")
        return [item]

    return query.all()


# --- AGENDA POR MÉDICO (GET) ---
@router.get("/doctor/{id_doctor}", response_model=List[ScheduleResponse])
def get_doctor_schedules(
        id_doctor: int,
        db_oper: Session = Depends(get_db_operative),
        current_user: dict = Depends(RequireRole(["Talento Humano", "Médico", "Paciente"]))
):
    return db_oper.query(Agenda).filter(Agenda.id_doctor == id_doctor).all()


# --- ACTUALIZAR AGENDA (PUT) ---
@router.put("/{id_agenda}", response_model=ScheduleResponse)
def update_schedule(
        id_agenda: int,
        payload: ScheduleCreate,
        db_oper: Session = Depends(get_db_operative),
        current_user: dict = Depends(RequireRole(["Talento Humano", "Médico"]))
):
    db_agenda = db_oper.query(Agenda).filter(Agenda.id_agenda == id_agenda).first()
    if not db_agenda:
        raise HTTPException(status_code=404, detail="Registro de agenda no encontrado")

    # Validación de solapamiento excluyendo el registro actual
    conflict = db_oper.query(Agenda).filter(
        Agenda.id_doctor == payload.id_doctor,
        Agenda.fecha == payload.fecha,
        Agenda.id_agenda != id_agenda,
        Agenda.estado == 1,
        Agenda.hora_inicio < payload.hora_fin,
        Agenda.hora_fin > payload.hora_inicio
    ).first()

    if conflict:
        raise HTTPException(status_code=400, detail="El nuevo horario se cruza con otro bloque existente")

    for key, value in payload.model_dump().items():
        setattr(db_agenda, key, value)

    db_oper.commit()
    db_oper.refresh(db_agenda)
    return db_agenda


# --- ELIMINAR AGENDA (DELETE) ---
@router.delete("/{id_agenda}", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule(
        id_agenda: int,
        db_oper: Session = Depends(get_db_operative),
        current_user: dict = Depends(RequireRole(["Talento Humano"]))
):
    """Solo Talento Humano puede eliminar bloques de agenda por motivos de auditoría."""
    db_agenda = db_oper.query(Agenda).filter(Agenda.id_agenda == id_agenda).first()
    if not db_agenda:
        raise HTTPException(status_code=404, detail="No existe el registro")

    db_oper.delete(db_agenda)
    db_oper.commit()
    return None


# --- GENERAR SLOTS (GET) ---
@router.get("/generate-slots/{id_doctor}", response_model=List[TimeSlot])
def generate_slots(
        id_doctor: int,
        fecha: date,
        duracion_minutos: int = 20,
        db_oper: Session = Depends(get_db_operative),
        current_user: dict = Depends(RequireRole(["Talento Humano", "Médico", "Paciente"]))
):
    """
    Divide los bloques de agenda en slots de tiempo para que los pacientes puedan agendar citas.
    """
    agendas = db_oper.query(Agenda).filter(
        Agenda.id_doctor == id_doctor,
        Agenda.fecha == fecha,
        Agenda.estado == 1
    ).all()

    if not agendas:
        raise HTTPException(status_code=404, detail="No hay bloques de agenda para este día")

    all_slots = []
    for block in agendas:
        current_dt = datetime.combine(fecha, block.hora_inicio)
        end_dt = datetime.combine(fecha, block.hora_fin)

        while current_dt + timedelta(minutes=duracion_minutos) <= end_dt:
            slot_start = current_dt.time()
            current_dt += timedelta(minutes=duracion_minutos)
            slot_end = current_dt.time()
            all_slots.append(TimeSlot(hora_inicio=slot_start, hora_fin=slot_end, disponible=True))

    return all_slots