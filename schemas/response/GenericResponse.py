from typing import Generic, TypeVar, Optional

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status

T = TypeVar("T")

class Response(Generic[T]):
    def __init__(self, hasError: bool, message: str, data: Optional[T] = None):
        self.hasError = hasError
        self.message = message
        self.data = data

    @classmethod
    def ok(cls, data: T, message: str = "Operación exitosa") -> "Response[T]":
        return cls(False, message, data)

    @classmethod
    def error(cls, message: str) -> "Response[T]":
        return cls(True, message, None)
    
    def toHttpResponse(self, statusCode=status.HTTP_200_OK):
        return JSONResponse(
            status_code=statusCode,
            content=jsonable_encoder(self)
        )