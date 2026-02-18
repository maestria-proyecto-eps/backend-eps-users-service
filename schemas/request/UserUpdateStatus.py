from pydantic import BaseModel, Field


class UserUpdateStatus(BaseModel):
    status: int = Field(...,ge=0, le=32767)