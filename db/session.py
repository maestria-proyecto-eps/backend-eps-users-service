# db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base # Moderno

import os

BaseAdmin = declarative_base()      # Para Médicos, Personas, etc.
BaseOperative = declarative_base()   # Para Agenda, Citas, etc.

load_dotenv()

def get_url(prefix):

    user = os.getenv(f"{prefix}_USER")
    password = os.getenv(f"{prefix}_PASSWORD")
    host = os.getenv(f"{prefix}_HOST")
    port = os.getenv(f"{prefix}_PORT", "5432")
    db_name = os.getenv(f"{prefix}_NAME", "postgres")

    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

# Motores
engine_admin = create_engine(get_url("DB_ADMIN"))
engine_oper = create_engine(get_url("DB_OPER"))

# Fábricas de Sesiones
SessionAdmin = sessionmaker(autocommit=False, autoflush=False, bind=engine_admin)
SessionOper = sessionmaker(autocommit=False, autoflush=False, bind=engine_oper)

# Dependencias para los endpoints de FastAPI
def get_db_admin():
    db = SessionAdmin()
    try:
        yield db
    finally:
        db.close()

def get_db_oper():
    db = SessionOper()
    try:
        yield db
    finally:
        db.close()