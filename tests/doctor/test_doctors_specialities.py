import random
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

ID_PERSONA_EXISTENTE = 10123456
ID_MEDICO_SEMILLA = 80112457
ID_ESPECIALIDAD_EXISTENTE = 1
ID_ESPECIALIDAD_CARDIOLOGIA = 3


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "EPS API"


def test_get_doctors_list():
    response_total = client.get("/api/doctors")
    assert response_total.status_code == 200
    assert isinstance(response_total.json(), list)

    response_filter = client.get(f"/api/doctors/by-specialty/{ID_ESPECIALIDAD_EXISTENTE}")
    assert response_filter.status_code == 200
    assert isinstance(response_filter.json(), list)


def test_create_doctor_logic():
    licencia_nueva = random.randint(100000, 999999)
    payload = {
        "id_medico": ID_PERSONA_EXISTENTE,
        "num_licencia": licencia_nueva,
        "id_especialidad": ID_ESPECIALIDAD_EXISTENTE,
    }
    response = client.post("/api/doctors", json=payload)
    assert response.status_code in [201, 400, 404]

    if response.status_code == 201:
        data = response.json()
        assert data["id_medico"] == ID_PERSONA_EXISTENTE
        assert "num_licencia" in data


def test_update_doctor_specialty_flow():
    update_payload = {"id_especialidad": ID_ESPECIALIDAD_CARDIOLOGIA}
    response = client.put(
        f"/api/doctors/{ID_MEDICO_SEMILLA}/specialty", json=update_payload
    )

    if response.status_code == 200:
        assert response.json()["id_especialidad"] == ID_ESPECIALIDAD_CARDIOLOGIA
    else:
        assert response.status_code == 404

    payload_invalido = {"id_especialidad": 999}
    response_error = client.put(
        f"/api/doctors/{ID_MEDICO_SEMILLA}/specialty", json=payload_invalido
    )
    if response_error.status_code != 404:
        assert response_error.status_code == 400
        assert "especialidad" in response_error.json()["detail"].lower()


def test_get_specialties_catalog():
    response = client.get("/api/specialties")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 8


def test_get_specialty_remissions_data():
    response = client.get("/api/specialties/remission")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    if len(data) > 0:
        item = data[0]
        assert "nombre_remitida" in item
        assert "nombre_que_remite" in item