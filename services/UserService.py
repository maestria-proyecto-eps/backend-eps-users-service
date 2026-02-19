
from models import Usuario
from schemas.request import UserCreate
from schemas.response.UserResponse import UserResponse
from services.repositories import RolRepository
from services.repositories.UserRepository import UserRepository


class UserService:
    def __init__(self, repo: UserRepository, rolRepo: RolRepository):
        self.repo = repo
        self.rolRepo = rolRepo
    def AddUser(self, userData: UserCreate) -> UserResponse:
        # El Usuario no tiene Identificacion
        #if(self.repo.exists_by_id(userData.id)):
         #   raise ValueError("ID ya registrado")
        if(self.repo.exists_by_username(userData.username)):
            raise ValueError("Username ya registrado")
        if(not self.rolRepo.exists_by_id(userData.id_rol)):
            raise ValueError("El rol no existe")
        
        user = Usuario(**userData.dict())

        user = self.repo.create(user)
        self.repo.db.commit()
        self.repo.db.refresh(user)

        return UserResponse.model_validate(user)