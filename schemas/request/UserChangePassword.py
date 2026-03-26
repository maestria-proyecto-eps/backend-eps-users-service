from pydantic import BaseModel, Field


class UserChangePassword(BaseModel):
    oldPassword: str = Field(...,max_length=60)
    newPassword: str = Field(...,max_length=60)