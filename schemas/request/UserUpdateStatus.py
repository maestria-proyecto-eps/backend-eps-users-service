from pydantic import BaseModel, Field


class UserUpdateStatus(BaseModel):
    estado: int = Field(...,ge=0, le=1)