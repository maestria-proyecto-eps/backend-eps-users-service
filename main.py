from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.logger import setup_logging
from db.session import SessionLocal, engine
from db.session import Base

from routers import specialties, doctors

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

app.include_router(specialties.router)
app.include_router(doctors.router)

@app.get("/")
def root():
    """Root endpoint"""
    #logger.info("Root endpoint called")
    return {
        "message": "EPS API",
        "features": [
            "EPS management API"
        ],
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def root():
    """health endpoint"""
    return {
        "message": "ok"
    }
