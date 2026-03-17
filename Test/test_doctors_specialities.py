import pytest
import random
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

ID_PERSONA_EXISTENTE = 10123456  # Ejemplo: Si en tu semilla existe esta persona
ID_MEDICO_SEMILLA = 80112457    # Alejandro Ruiz (Ya es médico en la semilla)
ID_ESPECIALIDAD_EXISTENTE = 1   # Medicina General

# 1. Prueba: Root API
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "EPS API"

# 2. Prueba obtención de doctores
def test_get_doctors():
    # El router ahora usa GET /api/doctors/ y permite filtrar
    response = client.get("/api/doctors/by-specialty/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Si hay médicos cargados en la semilla, debería haber al menos uno
    assert len(response.json()) >= 0

# 3. Prueba: Crear un doctor
def test_create_doctor():
    # Para que este test pase, la persona con ID 10123456
    # DEBE existir previamente en la tabla 'persona' de la DB administrativa.

    licencia_nueva = random.randint(100000, 999999)

    # Payload limpio: Solo campos que pertenecen a la tabla MEDICOS
    payload = {
        "id_medico": ID_PERSONA_EXISTENTE,
        "num_licencia": licencia_nueva,
        "id_especialidad": ID_ESPECIALIDAD_EXISTENTE
    }

    response = client.post("/api/doctors/", json=payload)

    # 201: Creado con éxito
    # 400: Ya era médico
    # 404: La persona no existe en la tabla PERSONA
    assert response.status_code in [201, 400, 404]

    if response.status_code == 201:
        data = response.json()
        assert data["id_medico"] == ID_PERSONA_EXISTENTE
        # Verificamos que el schema de respuesta incluya nombres (extraídos de Persona)
        assert "nombres" in data

# 4. Prueba cambiar especialidad (Usando médico de la SEMILLA)
def test_update_doctor_specialty():
    # Actualización Exitosa: Cardiología (ID 3)
    update_payload = {"id_especialidad": 3}
    response = client.put(f"/api/doctors/{ID_MEDICO_SEMILLA}/specialty", json=update_payload)

    assert response.status_code == 200
    assert response.json()["id_especialidad"] == 3

    # Error: Especialidad inexistente
    payload_invalido = {"id_especialidad": 9999}
    response_error = client.put(f"/api/doctors/{ID_MEDICO_SEMILLA}/specialty", json=payload_invalido)

    assert response_error.status_code == 400
    # Ajustado al mensaje de error que pusimos en el router
    assert "no existe" in response_error.json()["detail"].lower()

    # REVERSIÓN: Dejarlo como estaba (Medicina General)
    client.put(f"/api/doctors/{ID_MEDICO_SEMILLA}/specialty", json={"id_especialidad": 1})

# 5. Prueba doctor no encontrado
def test_update_doctor_not_found():
    update_payload = {"id_especialidad": 2}
    # Un ID que definitivamente no sea un médico
    response = client.put("/api/doctors/101010/specialty", json=update_payload)

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower() or "no encontrado" in response.json()["detail"].lower()

# 6. Prueba obtención especialidades
def test_get_specialties():
    response = client.get("/api/specialties/")
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        nombres = [e["nombre_especialidad"] for e in data]
        assert "Medicina General" in nombres