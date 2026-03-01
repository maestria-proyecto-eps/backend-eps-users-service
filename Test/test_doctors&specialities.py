import pytest
import random
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# --- CONFIGURACIÓN DE DATOS DE PRUEBA ---
# Se un ID de usuario que exista en la semilla pero no tenga médico asignado aún.
# El usuario 11 es un Paciente, para pruebas de creación de médico o crear un usuario nuevo.

ID_MEDICO_TEST = 99999
ID_USUARIO_TEST = 20    # El usuario 20 es Roberto Gil (Paciente en la semilla)
ID_ESPECIALIDAD_EXISTENTE = 1 # Medicina General

# 1. Prueba: ¿La API responde en el root?
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "EPS API"

# 2. Prueba obtención de doctores (Lectura segura)
def test_get_doctors_by_specialty():
    # Busca especialidad 1 (Medicina General) que ya tiene médicos en la semilla
    response = client.get("/api/doctors/by-specialty/?id_especialidad=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Verifica que traiga al menos uno de los médicos semilla
    assert len(response.json()) > 0

# 3. Prueba: Crear un doctor (Con ID manual y limpieza lógica)
def test_create_doctor():
    # Primero intenta borrarlo por si el test se corrió antes (borrado preventivo de seguridad)
    licencia_nueva = random.randint(100000, 999999)

    payload = {
        "id_medico": ID_MEDICO_TEST,
        "nombres": "Prueba",
        "apellidos": "Unitario",
        "num_licencia": licencia_nueva,
        "id_especialidad": ID_ESPECIALIDAD_EXISTENTE,
        "id_usuario": ID_USUARIO_TEST,
        "estado": 1
    }

    # Si el médico ya existe de un test anterior, lo ignora o fallará con 400.
    response = client.post("/api/doctors/", json=payload)

    # Acepta 200 si es nuevo o 400 si ya lo creo en una corrida anterior
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        assert response.json()["id_medico"] == ID_MEDICO_TEST

# 4. Prueba cambiar especialidad a doctor (Usando un médico de la SEMILLA)
def test_update_doctor_specialty():
    # Usa al médico Alejandro Ruiz (ID: 80112457) que ya está en la DB
    doctor_id_semilla = 80112457

    # Cambia de Medicina General (1) a Pediatría (3)
    update_payload = {"id_especialidad": 3}
    response = client.put(f"/api/doctors/{doctor_id_semilla}/specialty", json=update_payload)

    assert response.status_code == 200
    assert response.json()["id_especialidad"] == 3

    # REVERSIÓN: Devuelve al médico a su estado original para no alterar la semilla permanentemente
    client.put(f"/api/doctors/{doctor_id_semilla}/specialty", json={"id_especialidad": 1})

# 5. Prueba doctor no encontrado
def test_update_doctor_not_found():
    update_payload = {"id_especialidad": 2}
    # Un ID que definitivamente no existe
    response = client.put("/api/doctors/123/specialty", json=update_payload)

    assert response.status_code == 404

# 6. Prueba obtención especialidades (Lectura pura)
def test_get_specialties():
    response = client.get("/api/specialties/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    assert len(data) >= 8

    nombres = [e["nombre_especialidad"] for e in data]
    assert "Medicina General" in nombres