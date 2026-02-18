from fastapi import APIRouter, Depends

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
    return service.create_user(user)
