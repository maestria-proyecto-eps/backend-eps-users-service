import pytest
from fastapi.testclient import TestClient
from main import app
from datetime import date

client = TestClient(app)

ID_DOCTOR_EXISTENTE = 80112457
ID_ESPECIALIDAD_EXISTENTE = 1
FECHA_TEST = "2026-05-20"

# 1. Test: Crear horario
def test_create_schedule():
    # Se ajusta el campo a 'id_doctor' según el nuevo schema y modelo
    payload = {
        "id_doctor": ID_DOCTOR_EXISTENTE,
        "id_especialidad": ID_ESPECIALIDAD_EXISTENTE,
        "fecha": FECHA_TEST,
        "hora_inicio": "08:00:00",
        "hora_fin": "10:00:00",
        "estado": 1
    }
    response = client.post("/api/schedules/", json=payload)

    # El código ahora valida contra la DB Administrativa primero
    # Se acepta 200 si es nuevo o 400 si ya existe el bloque en la DB Operativa
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        assert response.json()["id_doctor"] == ID_DOCTOR_EXISTENTE

# 2. Test: Validar existencia del médico (DB Administrativa)
def test_create_schedule_doctor_not_found():
    # Se prueba con un ID que difícilmente exista en la DB Administrativa
    payload = {
        "id_doctor": 999999999,
        "id_especialidad": 1,
        "fecha": FECHA_TEST,
        "hora_inicio": "14:00:00",
        "hora_fin": "15:00:00"
    }
    response = client.post("/api/schedules/", json=payload)

    # Se verifica que el código responda con 404 por la validación de db_admin
    assert response.status_code == 404
    assert "no existe en la base de datos administrativa" in response.json()["detail"]

# 3. Test: Validar Solapamiento (DB Operativa - Debe fallar con 400)
def test_create_schedule_overlap():
    # Se intenta crear un bloque que colisiona con el del primer test (08:00 - 10:00)
    payload_conflictivo = {
        "id_doctor": ID_DOCTOR_EXISTENTE,
        "id_especialidad": ID_ESPECIALIDAD_EXISTENTE,
        "fecha": FECHA_TEST,
        "hora_inicio": "09:00:00",
        "hora_fin": "11:00:00",
        "estado": 1
    }
    response = client.post("/api/schedules/", json=payload_conflictivo)

    assert response.status_code == 400
    assert "Conflicto" in response.json()["detail"]

# 4. Test: Generar Slots de 20 minutos
def test_generate_slots():
    # El bloque creado en test_create_schedule es de 120 minutos (8 a 10)
    # 120 / 20 = 6 slots. Se ajusta el parámetro a id_doctor
    response = client.get(f"/api/schedules/generate-slots/{ID_DOCTOR_EXISTENTE}?fecha={FECHA_TEST}&duracion_minutos=20")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    # Se valida la cantidad de intervalos de 20 minutos generados
    assert len(data) == 6
    assert data[0]["hora_inicio"] == "08:00:00"
    assert data[0]["hora_fin"] == "08:20:00"

# 5. Test: Borrado de horario
def test_delete_schedule():
    # Primero se obtiene el id de la agenda creada para ese doctor
    get_response = client.get(f"/api/schedules/doctor/{ID_DOCTOR_EXISTENTE}")
    schedules = get_response.json()

    if schedules:
        id_a_borrar = schedules[0]["id_agenda"]
        delete_response = client.delete(f"/api/schedules/{id_a_borrar}")
        assert delete_response.status_code == 204