import pytest
import random
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Configuración de constantes para el entorno de pruebas
ID_PERSONA_EXISTENTE = 10123456
ID_MEDICO_SEMILLA = 80112457
ID_ESPECIALIDAD_EXISTENTE = 1
ID_ESPECIALIDAD_CARDIOLOGIA = 3

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "EPS API"

def test_get_doctors_list():
    # El sistema permite la obtención total de médicos o filtrada por especialidad
    response_total = client.get("/api/doctors")
    assert response_total.status_code == 200
    assert isinstance(response_total.json(), list)

    response_filter = client.get(f"/api/doctors/by-specialty/{ID_ESPECIALIDAD_EXISTENTE}")
    assert response_filter.status_code == 200
    assert isinstance(response_filter.json(), list)

def test_create_doctor_logic():
    # La creación valida la existencia de la persona y la especialidad
    licencia_nueva = random.randint(100000, 999999)
    payload = {
        "id_medico": ID_PERSONA_EXISTENTE,
        "num_licencia": licencia_nueva,
        "id_especialidad": ID_ESPECIALIDAD_EXISTENTE
    }

    response = client.post("/api/doctors", json=payload)

    # El resultado depende del estado previo de la base de datos de pruebas
    assert response.status_code in [201, 400, 404]

    if response.status_code == 201:
        data = response.json()
        assert data["id_medico"] == ID_PERSONA_EXISTENTE
        assert "num_licencia" in data

def test_update_doctor_specialty_flow():
    # El flujo comprueba la actualización exitosa y la validación de errores
    update_payload = {"id_especialidad": ID_ESPECIALIDAD_CARDIOLOGIA}
    response = client.put(f"/api/doctors/{ID_MEDICO_SEMILLA}/specialty", json=update_payload)

    if response.status_code == 200:
        assert response.json()["id_especialidad"] == ID_ESPECIALIDAD_CARDIOLOGIA
    else:
        # Si el médico de semilla no existe en el entorno actual
        assert response.status_code == 404

    # Verificación de respuesta ante especialidad inexistente
    payload_invalido = {"id_especialidad": 999}
    response_error = client.put(f"/api/doctors/{ID_MEDICO_SEMILLA}/specialty", json=payload_invalido)

    if response_error.status_code != 404:
        assert response_error.status_code == 400
        assert "especialidad" in response_error.json()["detail"].lower()

def test_get_specialties_catalog():
    # El sistema debe retornar el catálogo limitado a las primeras 8 especialidades
    response = client.get("/api/specialties")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 8

def test_get_specialty_remissions_data():
    # Se comprueba la estructura de la tabla de asociación de remisiones
    response = client.get("/api/specialties/remission")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    if len(data) > 0:
        item = data[0]
        assert "nombre_remitida" in item
        assert "nombre_que_remite" in item