from fastapi import Depends
from db.session import get_db
from services.UserService import UserService
from services.PersonaService import PersonaService
from services.repositories.UserRepository import UserRepository
from services.repositories.RolRepository import RolRepository
from services.repositories.PersonaRepository import PersonaRepository

#Repositories
def getRolRepository(db = Depends(get_db))-> RolRepository:
    return RolRepository(db)
def getUserRepository(db = Depends(get_db))-> UserRepository:
    return UserRepository(db)
def getPersonaRepository(db=Depends(get_db)) -> PersonaRepository:
    return PersonaRepository(db)

#Services
def getUserService(userRepo = Depends(getUserRepository), rolRepo = Depends(getRolRepository), personaRepo = Depends(getPersonaRepository)) -> UserService:
    return UserService(userRepo, rolRepo, personaRepo)
def getPersonaService(
    personaRepo=Depends(getPersonaRepository)) -> PersonaService:
    return PersonaService(personaRepo)
