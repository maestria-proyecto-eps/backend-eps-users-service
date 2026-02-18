
from models import Usuario
from schemas.request import UserCreate
from services.repositories import RolRepository
from services.repositories.UserRepository import userRepository


class userService:
    def __init__(self, repo: userRepository, rolRepo: RolRepository):
        self.repo = repo
        self.rolRepo = rolRepo
    def AddUser(self, userData: UserCreate) -> int:
        if(self.repo.exists_by_id(userData.id)):
            raise ValueError("ID ya registrado")
        if(self.repo.exists_by_id(userData.username)):
            raise ValueError("Username ya registrado")
        if(not self.rolRepo.exists_by_id(userData.id_rol)):
            raise ValueError("El rol no existe")
        
        user = Usuario(**userData.dict())

        user = self.repo.create(user)
        self.repo.db.commit()
        self.repo.db.refresh(user)

        return user.id