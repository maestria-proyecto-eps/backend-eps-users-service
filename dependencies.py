from fastapi import Depends
from db.session import get_db
from services.UserService import UserService
from services.repositories.UserRepository import UserRepository
from services.repositories.RolRepository import RolRepository

#Repositories
def getRolRepository(db = Depends(get_db))-> RolRepository:
    return RolRepository(db)
def getUserRepository(db = Depends(get_db))-> UserRepository:
    return UserRepository(db)

#Services
def getUserService(userRepo = Depends(getUserRepository), rolRepo = Depends(getRolRepository)) -> UserService:
    return UserService(userRepo, rolRepo)