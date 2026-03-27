from sqlalchemy import NullPool, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

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
    f"postgresql+psycopg2://{settings.DB_OPERATIVE_USER}:{settings.DB_OPERATIVE_PASSWORD}@"
    f"{settings.DB_OPERATIVE_HOST}:{settings.DB_OPERATIVE_PORT}/{settings.DB_OPERATIVE_NAME}?sslmode=require"
)

operative_engine = create_engine(OPERATIVE_URL, poolclass=NullPool)
SessionOperative = sessionmaker(autocommit=False, autoflush=False, bind=operative_engine)
BaseOperative = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_operative():
    db = SessionOperative()
    try:
        yield db
    finally:
        db.close()