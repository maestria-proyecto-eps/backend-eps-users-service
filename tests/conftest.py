from pathlib import Path
import os
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Variables de entorno para pruebas
os.environ.setdefault("DB_ADMIN_USER", "test")
os.environ.setdefault("DB_ADMIN_PASSWORD", "test")
os.environ.setdefault("DB_ADMIN_HOST", "localhost")
os.environ.setdefault("DB_ADMIN_PORT", "5432")
os.environ.setdefault("DB_ADMIN_NAME", "test_db")
os.environ.setdefault("DB_OP_USER", "test")
os.environ.setdefault("DB_OP_PASSWORD", "test")
os.environ.setdefault("DB_OP_HOST", "localhost")
os.environ.setdefault("DB_OP_PORT", "5432")
os.environ.setdefault("DB_OP_NAME", "test_db")
os.environ.setdefault("JWT_EXPIRES_MINUTES", "60")
os.environ.setdefault("JWT_SECRET", "test-secret")
os.environ.setdefault("JWT_ALGORITHM", "HS256")

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from main import app
from db.session import Base, BaseOperative, get_db, get_db_audit, get_db_operative, get_db_operative_audit
from core.dependencias import get_usuario_actual
from core.auth_utils import get_current_user_id

# ── Un solo engine SQLite en memoria para ambas bases ────────────────────────
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Usuario ficticio que bypasea auth ─────────────────────────────────────────
class _FakeRol:
    nombre_rol = "Administrador"


class _FakeUsuario:
    id_usuario = 1
    id_rol = 1
    rol = _FakeRol()


def override_get_current_user_id():
    return 1


def override_get_usuario_actual():
    return _FakeUsuario()


# ── Setup global de la sesión de pruebas ─────────────────────────────────────
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Crear tablas de AMBOS declarative_base en el mismo engine SQLite
    Base.metadata.create_all(bind=engine)
    BaseOperative.metadata.create_all(bind=engine)

    # Overrides de base de datos (admin y operativa apuntan al mismo SQLite)
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_db_audit] = override_get_db
    app.dependency_overrides[get_db_operative] = override_get_db
    app.dependency_overrides[get_db_operative_audit] = override_get_db

    # Overrides de autenticación
    app.dependency_overrides[get_current_user_id] = override_get_current_user_id
    app.dependency_overrides[get_usuario_actual] = override_get_usuario_actual

    yield

    Base.metadata.drop_all(bind=engine)
    BaseOperative.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


# ── Fixtures compartidos ──────────────────────────────────────────────────────
@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture
def test_rol():
    from models.Rol import Role
    db = TestingSessionLocal()
    existing = db.query(Role).filter(Role.id_rol == 1).first()
    if existing:
        db.close()
        yield existing
        return

    rol = Role(id_rol=1, nombre_rol="Administrador")
    db.add(rol)
    db.commit()
    db.refresh(rol)
    yield rol

    from models.Usuario import Usuario
    db.query(Usuario).filter(Usuario.id_rol == 1).delete()
    db.commit()
    db.delete(rol)
    db.commit()
    db.close()


@pytest.fixture
def test_persona(test_rol):
    from models.Persona import Persona
    db = TestingSessionLocal()
    persona = Persona(
        num_documento=123456789,
        nombres="Laura",
        apellidos="Gomez",
    )
    db.add(persona)
    db.commit()
    db.refresh(persona)
    yield persona
    db.delete(persona)
    db.commit()
    db.close()


@pytest.fixture
def test_user(test_persona, test_rol):
    from models.Usuario import Usuario
    db = TestingSessionLocal()
    usuario = Usuario(
        num_documento=123456789,
        password="abc123456",
        id_rol=1,
        estado=True,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    yield usuario
    db.delete(usuario)
    db.commit()
    db.close()


@pytest.fixture
def test_doctor():
    """Doctor de semilla necesario para los tests de schedules."""
    from models.Persona import Persona
    from models.doctor import Doctor
    db = TestingSessionLocal()

    # Doctor FK apunta a persona.num_documento, hay que crearla primero
    persona = Persona(
        num_documento=80112457,
        nombres="Doctor",
        apellidos="Semilla",
    )
    db.add(persona)
    db.commit()

    doctor = Doctor(
        id_medico=80112457,
        num_licencia=999999,
        id_especialidad=1,
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    yield doctor

    from models.schedule import Agenda
    db.query(Agenda).filter(Agenda.id_doctor == 80112457).delete()
    db.commit()
    db.delete(doctor)
    db.commit()
    db.delete(persona)
    db.commit()
    db.close()