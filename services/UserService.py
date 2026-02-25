
from models.Usuario import Usuario
from schemas.request import UserCreate
from schemas.response.GenericResponse import Response
from schemas.response.UserResponse import UserResponse
from services.repositories import RolRepository
from services.repositories.UserRepository import UserRepository
from services.helpers.security import security


class UserService:
    def __init__(self, repo: UserRepository, rolRepo: RolRepository):
        self.repo = repo
        self.rolRepo = rolRepo
    def AddUser(self, userData: UserCreate):
        if(self.repo.exists_by_numId(userData.num_documento)):
            return Response.error("Número de identificación ya registrado")
        if(not self.rolRepo.exists_by_id(userData.id_rol)):
            return Response.error("Rol no registrado")
        user = Usuario(**userData.dict())

        user.estado=1
        #user.password = security.hash_password(user.password)    #Se hashea la password


        self.repo.add_user(user)
        self.repo.db.commit()
        self.repo.db.refresh(user)

        return Response.ok(UserResponse.model_validate(user),"Usuario creado exitosamente")
    
    def GetUserById(self, id: int):
        user = self.repo.get_by_id(id)
        if(user == None):
            return Response.error("usuario no encontrado")
        return Response.ok(UserResponse.model_validate(user),"Usuario obtenido exitosamente")
    def DeleteUserById(self, id:int):
        user = self.repo.get_by_id(id)
        if(user == None):
            return Response.error("usuario no encontrado")
        if(user.estado==0):
            return Response.error("usuario ya se encuentra inactivo")
        user.estado=0
        self.repo.db.commit()
        return Response.ok(None,"usuario desactivado exitosamente")