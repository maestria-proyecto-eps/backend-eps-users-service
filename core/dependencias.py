from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from core.config import settings # Asegúrate de tener JWT_SECRET en tu .env

# Apuntamos la URL de Swagger al servicio de Auth para que el botón "Authorize" funcione
end_protegido = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/api/auth/login") # Ajusta el puerto al del auth-service

def get_usuario_actual(token: str = Depends(end_protegido)):
    """Valida el token sin consultar la base de datos, usando solo el payload"""
    try:
        datos = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

        # Validamos que traiga el rol
        if datos.get("role") is None or datos.get("num_documento") is None:
            raise HTTPException(status_code=401, detail="Token inválido o incompleto")

        # Retornamos el diccionario con los datos del token
        return datos
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expirado o inválido")

class RequireRole:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user_data: dict = Depends(get_usuario_actual)):
        user_role = user_data.get("role")

        if user_role not in self.allowed_roles and user_role != "Administrador":
            raise HTTPException(
                status_code=403,
                detail={
                    "hasError": True,
                    "Message": f"Acceso denegado. Se requiere uno de estos roles: {self.allowed_roles}",
                    "Data": None
                }
            )
        return user_data