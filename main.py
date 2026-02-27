from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text # Importante para la limpieza

from core.logger import setup_logging
from db.session import SessionLocal, engine
from db.base import Base

# Importar los modelos antes de create_all es VITAL
from models.specialty import Specialty
from models.doctor import Doctor
from routers import specialties, doctors

# --- BLOQUE DE LIMPIEZA Y SINCRONIZACIÓN ---
# Esto borra la tabla medicos y la crea de nuevo con id_usuario
# with engine.connect() as conn:
#     conn.execute(text("DROP TABLE IF EXISTS medicos CASCADE;"))
#     conn.commit()
#     print("Base de Datos: Tabla 'medicos' reseteada para actualizar columnas.")

# Crea todas las tablas definidas en los modelos importados
Base.metadata.create_all(bind=engine)
# ------------------------------------------

app = FastAPI(
    title="EPS API 2",
    description="EPS management API 2",
    version="0.1"
)

# Configuración de CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_logging()

# Inclusión de Routers
app.include_router(specialties.router)
app.include_router(doctors.router)

@app.get("/")
def root():
    return {
        "message": "EPS API",
        "docs": "/docs",
    }

@app.get("/health")
def health():
    return {"message": "ok"}

# CREACIÓN DE ESPECIALIDADES EN LA DB AL INICIO DE LA EJECUCION (YA EXISTEN CON ANTERIORIDAD)
def seed_data():
    db = SessionLocal()
    try:
        # Seed de Especialidades
        count = db.query(Specialty).count()
        if count == 0:
            nuevas_especialidades = [
                Specialty(nombre_especialidad="Medicina General", requiere_remision=False, dependencia="Ninguna"),
                Specialty(nombre_especialidad="Pediatría", requiere_remision=False, dependencia="Ninguna"),
                Specialty(nombre_especialidad="Cardiología", requiere_remision=True, dependencia="Medicina Interna"),
                Specialty(nombre_especialidad="Ginecología", requiere_remision=False, dependencia="Ninguna"),
                Specialty(nombre_especialidad="Dermatología", requiere_remision=True, dependencia="Medicina General"),
                Specialty(nombre_especialidad="Neurología", requiere_remision=True, dependencia="Medicina Interna"),
                Specialty(nombre_especialidad="Psiquiatría", requiere_remision=False, dependencia="Ninguna"),
                Specialty(nombre_especialidad="Ortopedia", requiere_remision=True, dependencia="Medicina General"),
            ]
            db.add_all(nuevas_especialidades)
            db.commit()
    except Exception as e:
        print(f" Error en seed: {e}")
    finally:
        db.close()

# Ejecutar el seed al iniciar
seed_data()