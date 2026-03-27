from pathlib import Path
import sys, os

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
    
# DB Administrativa
os.environ.setdefault("DB_ADMIN_USER", "test")
os.environ.setdefault("DB_ADMIN_PASSWORD", "test")
os.environ.setdefault("DB_ADMIN_HOST", "localhost")
os.environ.setdefault("DB_ADMIN_PORT", "5432")
os.environ.setdefault("DB_ADMIN_NAME", "test_db")
# DB Operativa
os.environ.setdefault("DB_OP_USER", "test")
os.environ.setdefault("DB_OP_PASSWORD", "test")
os.environ.setdefault("DB_OP_HOST", "localhost")
os.environ.setdefault("DB_OP_PORT", "5432")
os.environ.setdefault("DB_OP_NAME", "test_db")
# JWT
os.environ.setdefault("JWT_EXPIRES_MINUTES", "60")
os.environ.setdefault("JWT_SECRET", "test-secret")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
import pytest
from main import app

@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()