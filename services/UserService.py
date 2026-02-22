
from models.Usuario import Usuario
from schemas.request import UserCreate
from schemas.response.GenericResponse import Response
from schemas.response.UserResponse import UserResponse
from services.repositories import RolRepository
from services.repositories.UserRepository import UserRepository


class UserService:
    def __init__(self, repo: UserRepository, rolRepo: RolRepository):
        self.repo = repo
        self.rolRepo = rolRepo
    def AddUser(self, userData: UserCreate):
        if(self.repo.exists_by_username(userData.username)):
            return Response.error("Username ya registrado")
        if(not self.rolRepo.exists_by_id(userData.id_rol)):
            return Response.error("Rol no registrado")
        user = Usuario(**userData.dict())

        user.estado=1

        self.repo.add_user(user)
        self.repo.db.commit()
        self.repo.db.refresh(user)

        return Response.ok(UserResponse.model_validate(user),"Usuario creado exitosamente")
    
    def GetUserById(self, id: int):
        user = self.repo.get_by_id(id)
        if(user == None):
            return Response.error("usuario no encontrado")
        return Response.ok(UserResponse.model_validate(user),"Usuario obtenido exitosamente")