from typing import Generic, TypeVar, List
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginatedResponse(GenericModel, Generic[T]):
    items: List[T]
    total: int
    pagina: int
    tamPagina: int
    totalPaginas: int