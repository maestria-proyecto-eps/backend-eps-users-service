from fastapi import APIRouter, Depends,status

from dependencies import getUserService
from schemas.request.UserCreate import UserCreate
from schemas.response.UserResponse import UserResponse
from services import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserResponse)
def createUser(
    user: UserCreate,
    service: UserService = Depends(getUserService)
):
    model = service.AddUser(user)
    if(model.hasError):
        return model.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return model.toHttpResponse(status.HTTP_201_CREATED)

@router.get("/{id}", response_model=UserResponse)
def createUser(
    id: int,
    service: UserService = Depends(getUserService)
):
    model = service.GetUserById(id)
    if(model.hasError):
        return model.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return model.toHttpResponse(status.HTTP_201_CREATED)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def createUser(
    id: int,
    service: UserService = Depends(getUserService)
):
    model = service.DeleteUserById(id)
    if(model.hasError):
        return model.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return model.toHttpResponse(status.HTTP_204_NO_CONTENT)
