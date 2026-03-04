from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from models.Rol import Role
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from main import app
from db.session import Base, get_db

# Base de datos en memoria
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()
    
@pytest.fixture
def test_rol():
    db = TestingSessionLocal()
    rol = Role(
        id_rol=1,
        nombre_rol="Administrador"
    )
    db.add(rol)
    db.commit()
    db.refresh(rol)
    return rol
    
   

@pytest.fixture
def test_usuario(test_rol):
    from models.Usuario import Usuario
    db = TestingSessionLocal()

    usuario = Usuario(
        id_usuario=2,
        num_documento=123456789,
        password="abc123456",
        id_rol=1,
        estado=1
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario


@pytest.fixture()
def client():
    return TestClient(app)
