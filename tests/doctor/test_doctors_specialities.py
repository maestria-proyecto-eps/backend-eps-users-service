import pytest
from unittest.mock import MagicMock
from main import app
from db.session import get_db
from core.dependencias import get_usuario_actual

# Importamos los modelos
from models.doctor import Doctor
from models.Persona import Persona
from models.specialty import Specialty

# ---------------------------------------------------------
# FIXTURE PARA MOCKEAR LA BASE DE DATOS
# ---------------------------------------------------------
@pytest.fixture
def mock_db():
    """Simula la sesión de la base de datos en cada test"""
    session = MagicMock()
    app.dependency_overrides[get_db] = lambda: session
    yield session

# ---------------------------------------------------------
# PRUEBAS DE HISTORIAS DE USUARIO
# ---------------------------------------------------------

def test_crear_doctor_exitoso_como_hr(client, mock_db):
    """HU: Registrar doctores (Solo Talento Humano)"""
    # 1. Simulamos el rol de Talento Humano
    app.dependency_overrides[get_usuario_actual] = lambda: {
        "id_usuario": 1, "num_documento": 10123456, "role": "Talento Humano"
    }

    # 2. Preparamos los datos mockeados
    # Añadimos nombres y apellidos para evitar el ResponseValidationError
    persona_existente = Persona(
        num_documento=10123456,
        nombres="Juan",
        apellidos="Pérez"
    )
    especialidad_existente = Specialty(id_especialidad=1, nombre_especialidad="General")

    def side_effect(model):
        q = MagicMock()
        if model == Persona:
            q.filter.return_value.first.return_value = persona_existente
        elif model == Doctor:
            q.filter.return_value.first.return_value = None # No hay duplicados
        elif model == Specialty:
            q.filter.return_value.first.return_value = especialidad_existente
        return q

    mock_db.query.side_effect = side_effect

    # 3. Mockear el comportamiento de 'refresh' para inyectar los datos de Persona en el Doctor
    # Esto simula la carga de la relación en SQLAlchemy
    def mock_refresh(instance):
        instance.nombres = "Juan"
        instance.apellidos = "Pérez"
        instance.id_medico = 10123456

    mock_db.refresh.side_effect = mock_refresh

    payload = {
        "id_medico": 10123456,
        "num_licencia": 12345,
        "id_especialidad": 1
    }

    response = client.post("/api/doctors", json=payload)

    # 4. Validaciones
    assert response.status_code == 201
    data = response.json()
    assert data["id_medico"] == 10123456
    assert data["nombres"] == "Juan"
    assert data["apellidos"] == "Pérez"


def test_crear_doctor_denegado_como_paciente(client, mock_db):
    """HU: Seguridad (Un paciente no puede registrar doctores)"""
    # 1. Simulamos el rol de Paciente
    app.dependency_overrides[get_usuario_actual] = lambda: {
        "id_usuario": 2, "num_documento": 987654, "role": "Paciente"
    }

    payload = {"id_medico": 10123456, "num_licencia": 12345, "id_especialidad": 1}
    response = client.post("/api/doctors", json=payload)

    # El RequireRole debe lanzar 403
    assert response.status_code == 403


def test_get_specialties_catalog(client, mock_db):
    """HU: Consulta de especialidades (Acceso para Pacientes)"""
    app.dependency_overrides[get_usuario_actual] = lambda: {"role": "Paciente"}

    # Mock de la lista de especialidades
    mock_query = MagicMock()
    mock_query.limit.return_value.all.return_value = [
        Specialty(id_especialidad=1, nombre_especialidad="Pediatría"),
        Specialty(id_especialidad=2, nombre_especialidad="Cardiología")
    ]
    mock_db.query.return_value = mock_query

    response = client.get("/api/specialties/")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_doctor_specialty_unauthorized(client, mock_db):
    """HU: Seguridad (Un médico no puede editar especialidades)"""
    app.dependency_overrides[get_usuario_actual] = lambda: {"role": "Médico"}

    update_payload = {"id_especialidad": 3}
    response = client.put("/api/doctors/80112457/specialty", json=update_payload)

    assert response.status_code == 403