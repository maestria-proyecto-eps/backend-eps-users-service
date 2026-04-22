from pathlib import Path
import sys
import pytest
from fastapi.testclient import TestClient

# 1. Configuración de rutas (lo que ya tenías)
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from main import app # Importar después de configurar el path

# 2. Cliente de pruebas único para todos los archivos
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# 3. Limpieza automática de dependencias (Tu red de seguridad)
@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    """
    Se ejecuta automáticamente antes y después de CADA test.
    Garantiza que un mock de 'Admin' no se filtre al siguiente test.
    """
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()