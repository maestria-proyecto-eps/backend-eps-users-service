from fastapi import APIRouter, Depends,status

from dependencies import getUserService
from schemas.request.UserChangePassword import UserChangePassword
from schemas.request.UserUpdateRole import UserUpdateRole
from schemas.request.UserCreate import UserCreate
from schemas.request.UserUpdateStatus import UserUpdateStatus
from schemas.request.UserUpdate import UserUpdate
from schemas.response.UserResponse import UserResponse
from schemas.response.GenericResponse import Response
from schemas.response.GenericPaginatedResponse import PaginatedResponse
from services import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=Response[UserResponse])
def createUser(
    user: UserCreate,
    service: UserService = Depends(getUserService)
):
    model = service.AddUser(user)
    if(model.hasError):
        status_code = model.statusCode if model.statusCode != status.HTTP_200_OK else status.HTTP_400_BAD_REQUEST
        return model.toHttpResponse(status_code)
    return model.toHttpResponse(status.HTTP_201_CREATED)

@router.get("/", response_model=Response[PaginatedResponse[UserResponse]])
def GetUsers(
    rol:int=None,estado:bool=None,num_document:int=None,
    nombres:str=None,apellidos:str=None,
    pag:int=1,cantidad:int=30,
    service: UserService = Depends(getUserService)
):
    model = service.GetUsers(rol,estado,num_document,nombres,apellidos,pag,cantidad)
    if(model.hasError):
        return model.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return model.toHttpResponse()

@router.get("/{id}", response_model=Response[UserResponse])
def getUser(
    id: int,
    service: UserService = Depends(getUserService)
):
    model = service.GetUserById(id)
    if(model.hasError):
        return model.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return model.toHttpResponse(status.HTTP_200_OK)

@router.put("/{id}", response_model=Response[UserResponse])
def UpdateUser(
    id: int,
    user: UserUpdate,
    service: UserService = Depends(getUserService)
):
    model = service.UpdateUserById(id,user)
    if(model.hasError):
        return model.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return model.toHttpResponse()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteUser(
    id: int,
    service: UserService = Depends(getUserService)
):
    model = service.DeleteUserById(id)
    if(model.hasError):
        return model.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return model.toHttpResponse(status.HTTP_204_NO_CONTENT)

@router.put("/{id}/change-role", response_model=Response[UserResponse])
def UpdateRoleUser(
    id: int,
    user: UserUpdateRole,
    service: UserService = Depends(getUserService)
):
    model = service.ChangeserRoleById(id,user)
    if(model.hasError):
        return model.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return model.toHttpResponse()
@router.put("/{id}/change-status", response_model=Response[UserResponse])
def UpdateStatusUser(
    id: int,
    user: UserUpdateStatus,
    service: UserService = Depends(getUserService)
):
    model = service.UpdateuserStatuById(id,user)
    if(model.hasError):
        return model.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return model.toHttpResponse()
@router.post("/{id}/reset-password", response_model=Response[UserResponse])
def UpdatePasswordUser(
    id: int,
    user: UserChangePassword,
    service: UserService = Depends(getUserService)
):
    model = service.UpdateUserPasswordById(id,user)
    if(model.hasError):
        return model.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return model.toHttpResponse()
