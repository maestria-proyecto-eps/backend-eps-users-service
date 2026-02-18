from fastapi import APIRouter, Depends

from dependencies import getUserService
from schemas.request import UserCreate
from services import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=int)
def createUser(
    user: UserCreate,
    service: UserService = Depends(getUserService)
):
    return service.create_user(user)
