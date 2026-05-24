from sqlalchemy import NullPool, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings
from fastapi import Depends
from core.auth_utils import get_current_user_id
from sqlalchemy import text
USER = settings.DB_ADMIN_USER
PASSWORD = settings.DB_ADMIN_PASSWORD
HOST = settings.DB_ADMIN_HOST
PORT = settings.DB_ADMIN_PORT
DBNAME = settings.DB_ADMIN_NAME

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

engine = create_engine(DATABASE_URL, poolclass=NullPool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

OPERATIVE_URL = (
    f"postgresql+psycopg2://{settings.DB_OP_USER}:{settings.DB_OP_PASSWORD}@"
    f"{settings.DB_OP_HOST}:{settings.DB_OP_PORT}/{settings.DB_OP_NAME}?sslmode=require"
)

operative_engine = create_engine(OPERATIVE_URL, poolclass=NullPool)
SessionOperative = sessionmaker(autocommit=False, autoflush=False, bind=operative_engine)
BaseOperative = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()       
    except Exception:
        db.rollback() 
        raise
    finally:
        db.close()
        
def get_db_operative():
    db = SessionOperative()
    try:
        yield db
        db.commit()       
    except Exception:
        db.rollback() 
        raise
    finally:
        db.close()

        
def get_db_audit(
    user_id: int = Depends(get_current_user_id)
):
    db = SessionLocal()

    try:
        db.execute(
            text("SET LOCAL my.app_user_id = :uid"),
            {"uid": str(user_id)}
        )
        yield db
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
        
def get_db_operative_audit(
    user_id: int = Depends(get_current_user_id)
):
    db = SessionOperative()

    try:
        db.execute(
            text("SET LOCAL my.app_user_id = :uid"),
            {"uid": str(user_id)}
        )
        yield db
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()