from fastapi import Depends
from db.session import get_db
from services.UserService import UserService
from services.repositories.UserRepository import UserRepository
from services.repositories.RolRepository import RolRepository
from services.EnfermeroService import EnfermeroService
from services.FarmaceutaService import FarmaceutaService
from services.repositories.EnfermeroRepository import EnfermeroRepository
from services.repositories.FarmaceutaRepository import FarmaceutaRepository

#Repositories
def getRolRepository(db = Depends(get_db))-> RolRepository:
    return RolRepository(db)
def getUserRepository(db = Depends(get_db))-> UserRepository:
    return UserRepository(db)
def getEnfermeroRepository(db=Depends(get_db)) -> EnfermeroRepository:
    return EnfermeroRepository(db)
def getFarmaceutaRepository(db=Depends(get_db)) -> FarmaceutaRepository:
    return FarmaceutaRepository(db)

#Services
def getUserService(userRepo = Depends(getUserRepository), rolRepo = Depends(getRolRepository)) -> UserService:
    return UserService(userRepo, rolRepo)
def getEnfermeroService(
    enfermeroRepo=Depends(getEnfermeroRepository),
    userRepo=Depends(getUserRepository)
) -> EnfermeroService:
    return EnfermeroService(enfermeroRepo, userRepo)
def getFarmaceutaService(
    farmaceutaRepo=Depends(getFarmaceutaRepository),
    userRepo=Depends(getUserRepository)
) -> FarmaceutaService:
    return FarmaceutaService(farmaceutaRepo, userRepo)
