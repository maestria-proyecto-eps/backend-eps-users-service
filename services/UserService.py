
import math

from models.Usuario import Usuario
from schemas.request import UserCreate, UserUpdateRole, UserUpdateStatus, UserUpdate, UserChangePassword
from schemas.response.GenericPaginatedResponse import PaginatedResponse
from schemas.response.GenericResponse import Response
from schemas.response.UserResponse import UserResponse
from services.repositories import RolRepository
from services.repositories.UserRepository import UserRepository
from services.helpers.security import Security


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
        user.password = Security.hash_password(user.password)


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
    def ChangeserRoleById(self, id:int, userData : UserUpdateRole):
        user = self.repo.get_by_id(id)
        if(user == None):
            return Response.error("usuario no encontrado")
        if(user.estado ==0):
            return Response.error("usuario desactivado")
        if(not self.rolRepo.exists_by_id(userData.id_rol)):
            return Response.error("Rol no registrado")
        user.id_rol=userData.id_rol
        self.repo.db.commit()
        self.repo.db.refresh(user)
        return Response.ok(UserResponse.model_validate(user),"usuario actualizado exitosamente")
    def UpdateuserStatuById(self, id:int, userData : UserUpdateStatus):
        user = self.repo.get_by_id(id)
        if(user == None):
            return Response.error("usuario no encontrado")
        if(user.estado<0 or user.estado >1):
            return Response.error("estado no valido")
        user.estado=userData.estado
        self.repo.db.commit()
        self.repo.db.refresh(user)
        return Response.ok(UserResponse.model_validate(user),"usuario actualizado exitosamente")
    def UpdateUserPasswordById(self, id:int, userData : UserChangePassword):
        user = self.repo.get_by_id(id)
        if(user == None):
            return Response.error("usuario no encontrado")
        if(user.estado ==0):
            return Response.error("usuario desactivado")
        if( not Security.verify_password(userData.oldPassword, user.password)):
            return Response.error("Contraseña no concuerda")
        user.password=Security.hash_password(userData.newPassword)
        self.repo.db.commit()
        self.repo.db.refresh(user)
        return Response.ok(UserResponse.model_validate(user),"usuario actualizado exitosamente")
    def UpdateUserById(self, id:int, userData : UserUpdate):
        user = self.repo.get_by_id(id)
        if(user == None):
            return Response.error("usuario no encontrado")
        if(user.estado ==0):
            return Response.error("usuario desactivado")
        if(not self.rolRepo.exists_by_id(userData.id_rol)):
            return Response.error("Rol no registrado")
        user.num_documento=userData.num_documento
        user.id_rol=userData.id_rol
        self.repo.db.commit()
        self.repo.db.refresh(user)
        return Response.ok(UserResponse.model_validate(user),"usuario actualizado exitosamente")
    def GetUsers(self, rol: int, estado: int, pag:int, cantidad: int):
        if(rol != None and not self.rolRepo.exists_by_id(rol)):
            return Response.error("Rol no registrado")
        if(estado != None and (estado >0 or estado >1)):
            return Response.error("Estado no registrado")
        usuarios, totalElem = self.repo.get_users(rol,estado,pag,cantidad)
        totalPags = math.ceil(totalElem / cantidad)
        return Response.ok(PaginatedResponse[UserResponse](
        data=[UserResponse.model_validate(u) for u in usuarios],
        page=pag,
        pages=totalPags),"Datos obtenidos exitosamente")