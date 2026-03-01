from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from models.schedule import Schedule
from schemas.schedule import ScheduleCreate, ScheduleResponse, TimeSlot
from typing import List, Optional
from datetime import datetime, timedelta, date, time

router = APIRouter(prefix="/api/schedules", tags=["Schedules"])

@router.post("/", response_model=ScheduleResponse)
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    # 1. Buscar si hay horarios que se solapen para el mismo médico y día
    overlap = db.query(Schedule).filter(
        Schedule.id_medico == schedule.id_medico,
        Schedule.dia_semana == schedule.dia_semana,
        # Lógica de solapamiento: (Inicio1 < Fin2) Y (Fin1 > Inicio2)
        Schedule.hora_inicio < schedule.hora_fin,
        Schedule.hora_fin > schedule.hora_inicio
    ).first()

    if overlap:
        raise HTTPException(
            status_code=400,
            detail=f"Conflicto de horario: Ya existe un registro para este médico que se solapa ({overlap.hora_inicio} - {overlap.hora_fin})"
        )

    # 2. Si no hay solapamiento, crear el registro
    db_schedule = Schedule(**schedule.model_dump())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@router.get("/", response_model=List[ScheduleResponse])
def get_schedules(id_horario: Optional[int] = None, db: Session = Depends(get_db)):
    """
    ### Obtener horarios
    - Si proporcionas **id_horario**, devuelve ese horario específico (en una lista).
    - Si no proporcionas nada, devuelve **todos** los horarios registrados.
    """
    query = db.query(Schedule)

    if id_horario:
        schedule = query.filter(Schedule.id_horario == id_horario).first()
        if not schedule:
            raise HTTPException(status_code=404, detail="Horario no encontrado")
        return [schedule] # Lo devolvemos en lista para mantener consistencia con el response_model

    return query.all()

@router.get("/doctor/{id_medico}", response_model=List[ScheduleResponse])
def get_doctor_schedules(id_medico: int, db: Session = Depends(get_db)):
    """
    ### Obtiene la agenda semanal de un médico.
    Devuelve todos los bloques de tiempo asignados al doctor con el ID proporcionado.
    """
    schedules = db.query(Schedule).filter(Schedule.id_medico == id_medico).all()

    if not schedules:
        # No se lanza 404 porque es válido que un doctor nuevo aún no tenga horarios
        return []

    return schedules

@router.put("/{id_horario}", response_model=ScheduleResponse)
def update_schedule(
        id_horario: int,
        payload: ScheduleCreate,
        db: Session = Depends(get_db)
):
    """
    ### Actualiza un bloque de horario existente.
    También valida que los nuevos tiempos no choquen con otros horarios del doctor.
    """
    # 1. Buscar el horario actual
    db_schedule = db.query(Schedule).filter(Schedule.id_horario == id_horario).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    # 2. Validación de coherencia
    if payload.hora_inicio >= payload.hora_fin:
        raise HTTPException(status_code=400, detail="La hora de inicio debe ser menor a la hora de fin")

    # 3. Validar solapamiento (EXCLUYENDO el horario que estamos editando actualmente)
    conflict = db.query(Schedule).filter(
        Schedule.id_medico == payload.id_medico,
        Schedule.dia_semana == payload.dia_semana,
        Schedule.id_horario != id_horario,
        Schedule.hora_inicio < payload.hora_fin,
        Schedule.hora_fin > payload.hora_inicio
    ).first()

    if conflict:
        raise HTTPException(
            status_code=400,
            detail=f"Conflicto: El nuevo horario se cruza con una asignación existente ({conflict.hora_inicio} - {conflict.hora_fin})"
        )

    # 4. Actualizar los campos
    for key, value in payload.model_dump().items():
        setattr(db_schedule, key, value)

    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@router.delete("/{id_horario}", status_code=204)
def delete_schedule(id_horario: int, db: Session = Depends(get_db)):
    """
    ### Elimina un bloque de horario.
    Libera el espacio en la agenda del médico.
    """
    db_schedule = db.query(Schedule).filter(Schedule.id_horario == id_horario).first()

    if not db_schedule:
        raise HTTPException(status_code=404, detail="El horario no existe")

    db.delete(db_schedule)
    db.commit()
    return None

@router.get("/generate-slots/{id_medico}", response_model=List[TimeSlot])
def generate_slots(id_medico: int, fecha: date, db: Session = Depends(get_db)):
    """
    ### Genera slots de citas basados en el horario del médico.
    Ejemplo: Si el médico trabaja de 08:00 a 09:00 con slots de 20 min,
    generará: 08:00-08:20, 08:20-08:40, 08:40-09:00.
    """
    # 1. Mapear el nombre del día
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    nombre_dia = dias[fecha.weekday()]

    # 2. Buscar el horario del médico para ese día
    schedule = db.query(Schedule).filter(
        Schedule.id_medico == id_medico,
        Schedule.dia_semana == nombre_dia
    ).first()

    if not schedule:
        raise HTTPException(status_code=404, detail="El médico no tiene horario asignado para este día")

    # 3. Lógica para fragmentar el tiempo
    slots = []
    # Convertimos a datetime para poder sumar minutos fácilmente
    current_dt = datetime.combine(fecha, schedule.hora_inicio)
    end_dt = datetime.combine(fecha, schedule.hora_fin)

    while current_dt + timedelta(minutes=schedule.duracion_slot_minutos) <= end_dt:
        slot_start = current_dt.time()
        current_dt += timedelta(minutes=schedule.duracion_slot_minutos)
        slot_end = current_dt.time()

        slots.append(TimeSlot(hora_inicio=slot_start, hora_fin=slot_end))

    return slots