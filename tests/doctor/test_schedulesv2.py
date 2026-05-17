from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

ID_DOCTOR_EXISTENTE = 80112457
ID_ESPECIALIDAD_EXISTENTE = 1
FECHA_TEST = "2026-05-20"

# Payload base que crea un bloque 08:00 - 10:00
PAYLOAD_BASE = {
    "id_doctor": ID_DOCTOR_EXISTENTE,
    "id_especialidad": ID_ESPECIALIDAD_EXISTENTE,
    "fecha": FECHA_TEST,
    "hora_inicio": "08:00:00",
    "hora_fin": "10:00:00",
    "estado": 1,
}


def _crear_agenda():
    """Crea la agenda base y retorna la respuesta."""
    return client.post("/api/schedules/", json=PAYLOAD_BASE)


def test_create_schedule(test_doctor):
    response = _crear_agenda()
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        assert response.json()["id_doctor"] == ID_DOCTOR_EXISTENTE


def test_create_schedule_doctor_not_found():
    payload = {
        "id_doctor": 999999999,
        "id_especialidad": 1,
        "fecha": FECHA_TEST,
        "hora_inicio": "14:00:00",
        "hora_fin": "15:00:00",
    }
    response = client.post("/api/schedules/", json=payload)
    assert response.status_code == 404
    assert "no existe en la base de datos administrativa" in response.json()["detail"]


def test_create_schedule_overlap(test_doctor):
    # Primero crea el bloque base
    _crear_agenda()

    # Luego intenta crear uno que solapa (09:00 - 11:00 choca con 08:00 - 10:00)
    payload_conflictivo = {
        "id_doctor": ID_DOCTOR_EXISTENTE,
        "id_especialidad": ID_ESPECIALIDAD_EXISTENTE,
        "fecha": FECHA_TEST,
        "hora_inicio": "09:00:00",
        "hora_fin": "11:00:00",
        "estado": 1,
    }
    response = client.post("/api/schedules/", json=payload_conflictivo)
    assert response.status_code == 400
    assert "Conflicto" in response.json()["detail"]


def test_generate_slots(test_doctor):
    # Crea el bloque base (08:00 - 10:00 = 120 min / 20 = 6 slots)
    _crear_agenda()

    response = client.get(
        f"/api/schedules/generate-slots/{ID_DOCTOR_EXISTENTE}"
        f"?fecha={FECHA_TEST}&duracion_minutos=20"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 6
    assert data[0]["hora_inicio"] == "08:00:00"
    assert data[0]["hora_fin"] == "08:20:00"


def test_delete_schedule(test_doctor):
    get_response = client.get(f"/api/schedules/doctor/{ID_DOCTOR_EXISTENTE}")
    assert get_response.status_code == 200
    schedules = get_response.json()

    if schedules:
        id_a_borrar = schedules[0]["id_agenda"]
        delete_response = client.delete(f"/api/schedules/{id_a_borrar}")
        assert delete_response.status_code == 204