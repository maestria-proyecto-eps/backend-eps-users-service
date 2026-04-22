import pytest
from unittest.mock import MagicMock
from main import app
from db.session import get_db, get_db_operative
from core.dependencias import get_usuario_actual
from models.schedule import Agenda
from models.doctor import Doctor
from datetime import date, time

# Constantes alineadas estrictamente con tu Schema
ID_DOCTOR_EXISTENTE = 80112457
ID_ESPECIALIDAD_EXISTENTE = 1
FECHA_TEST = "2026-05-20"

@pytest.fixture
def mock_sessions():
    """Simula las sesiones de DB Administrativa y Operativa"""
    admin_session = MagicMock()
    oper_session = MagicMock()
    app.dependency_overrides[get_db] = lambda: admin_session
    app.dependency_overrides[get_db_operative] = lambda: oper_session
    return admin_session, oper_session

# 1. Test: Crear horario (EXITOSO)
def test_create_schedule(client, mock_sessions):
    db_admin, db_oper = mock_sessions
    app.dependency_overrides[get_usuario_actual] = lambda: {"role": "Talento Humano"}

    # Mock: El doctor existe en Admin y NO hay solapamiento en Operativa
    db_admin.query.return_value.filter.return_value.first.return_value = Doctor(id_medico=ID_DOCTOR_EXISTENTE)
    db_oper.query.return_value.filter.return_value.first.return_value = None

    # Mock para el ID generado al guardar y devolver el objeto creado
    db_oper.refresh.side_effect = lambda x: setattr(x, "id_agenda", 1)

    payload = {
        "id_doctor": ID_DOCTOR_EXISTENTE,
        "id_especialidad": ID_ESPECIALIDAD_EXISTENTE,
        "fecha": FECHA_TEST,
        "hora_inicio": "08:00:00",
        "hora_fin": "10:00:00",
        "estado": 1
    }
    response = client.post("/api/schedules/", json=payload)

    assert response.status_code == 201
    assert response.json()["id_doctor"] == ID_DOCTOR_EXISTENTE

# 2. Test: Validación de Horas (Error de Pydantic - hora_inicio >= hora_fin)
def test_create_schedule_invalid_hours(client, mock_sessions):
    app.dependency_overrides[get_usuario_actual] = lambda: {"role": "Médico"}

    payload = {
        "id_doctor": ID_DOCTOR_EXISTENTE,
        "id_especialidad": ID_ESPECIALIDAD_EXISTENTE,
        "fecha": FECHA_TEST,
        "hora_inicio": "10:00:00",
        "hora_fin": "08:00:00", # Error: inicio después del fin
        "estado": 1
    }
    response = client.post("/api/schedules/", json=payload)

    # Esto debería devolver 422 porque falla el model_validator de tu Schema
    assert response.status_code == 422
    assert "La hora de inicio debe ser anterior a la hora de fin" in response.text

# 3. Test: Médico no encontrado (404)
def test_create_schedule_doctor_not_found(client, mock_sessions):
    db_admin, _ = mock_sessions
    app.dependency_overrides[get_usuario_actual] = lambda: {"role": "Talento Humano"}

    db_admin.query.return_value.filter.return_value.first.return_value = None

    payload = {
        "id_doctor": 999,
        "id_especialidad": ID_ESPECIALIDAD_EXISTENTE,
        "fecha": FECHA_TEST,
        "hora_inicio": "14:00:00",
        "hora_fin": "15:00:00",
        "estado": 1
    }
    response = client.post("/api/schedules/", json=payload)

    assert response.status_code == 404
    assert "no existe en la base de datos administrativa" in response.json()["detail"]

# 4. Test: Solapamiento en Agenda (400)
def test_create_schedule_overlap(client, mock_sessions):
    db_admin, db_oper = mock_sessions
    app.dependency_overrides[get_usuario_actual] = lambda: {"role": "Talento Humano"}

    db_admin.query.return_value.filter.return_value.first.return_value = Doctor(id_medico=ID_DOCTOR_EXISTENTE)

    # Simulamos que la DB Operativa ya tiene un bloque a esa hora
    db_oper.query.return_value.filter.return_value.first.return_value = Agenda(
        id_agenda=1,
        hora_inicio=time(8,0),
        hora_fin=time(10,0)
    )

    payload = {
        "id_doctor": ID_DOCTOR_EXISTENTE,
        "id_especialidad": ID_ESPECIALIDAD_EXISTENTE,
        "fecha": FECHA_TEST,
        "hora_inicio": "09:00:00", # Choca
        "hora_fin": "11:00:00",
        "estado": 1
    }
    response = client.post("/api/schedules/", json=payload)

    assert response.status_code == 400
    assert "Conflicto" in response.json()["detail"]