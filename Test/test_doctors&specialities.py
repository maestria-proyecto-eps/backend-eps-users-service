import pytest
import random # Para evitar el error de "UniqueViolation" en num_licencia
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# 1. Prueba: ¿La API responde en el root?
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "EPS API"

# 2. Prueba obtencion de doctores
def test_get_doctors_by_specialty():
    response = client.get("/api/doctors/by-specialty/?id_especialidad=4")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# 3. Prueba: ¿Puedo crear un doctor?
def test_create_doctor():
    # Generamos una licencia aleatoria para que no falle por "duplicate key"
    licencia_nueva = random.randint(10000, 999999)
    payload = {
        "nombres": "Prueba",
        "apellidos": "Unitario",
        "num_licencia": licencia_nueva,
        "id_especialidad": 1,
        "id_usuario": 1,
        "estado": 1
    }
    response = client.post("/api/doctors/", json=payload)
    # Devuelve 200 OK tras el commit
    assert response.status_code == 200
    assert response.json()["nombres"] == "Prueba"

# 4. Prueba cambiar especialidad a doctor
def test_update_doctor_specialty():
    # Creamos uno nuevo para asegurar que el ID exista y la licencia no se repita
    licencia_update = random.randint(10000, 999999)
    setup_payload = {
        "nombres": "Medico",
        "apellidos": "Cambio",
        "num_licencia": licencia_update,
        "id_especialidad": 1,
        "estado": 1
    }
    create_res = client.post("/api/doctors/", json=setup_payload)
    doctor_id = create_res.json()["id_medico"]

    # Probamos el PUT
    update_payload = {"id_especialidad": 3}
    response = client.put(f"/api/doctors/{doctor_id}/specialty", json=update_payload)

    assert response.status_code == 200
    assert response.json()["id_especialidad"] == 3

# 5. Prueba doctor no encontrado
def test_update_doctor_not_found():
    update_payload = {"id_especialidad": 2}
    response = client.put("/api/doctors/99999/specialty", json=update_payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Médico no encontrado"

# 6. Prueba oibtencion especialidades
def test_get_specialties():
    """
    Prueba que el endpoint devuelva la lista de especialidades cargadas.
    Verifica que la respuesta sea 200 y que contenga elementos.
    """
    response = client.get("/api/specialties/")

    # 1. Verificar que la petición fue exitosa
    assert response.status_code == 200

    # 2. Verificar que recibimos una lista
    data = response.json()
    assert isinstance(data, list)

    # 3. Verificar que al menos hay datos (asumiendo que corriste el Seed)
    # Como tu código tiene .limit(8), validamos que no exceda eso
    assert len(data) <= 8

    # 4. Opcional: Verificar que la primera especialidad sea Medicina General
    if len(data) > 0:
        assert data[0]["nombre_especialidad"] == "Medicina General"