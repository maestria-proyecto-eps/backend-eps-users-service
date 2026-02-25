from sqlalchemy import BigInteger, Column, ForeignKey, Integer, SmallInteger, String, TIMESTAMP
from sqlalchemy.orm import  relationship
from db.session import Base 


class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario= Column(Integer, primary_key=True)
    num_documento= Column(BigInteger, nullable=False)
    password= Column(String(60), nullable=False)
    id_rol= Column(Integer,ForeignKey("roles.id_rol"), nullable=False)
    estado= Column(SmallInteger, nullable=False)
    intentos_login = Column(SmallInteger, nullable=False,default=0)
    tiempo_de_fallo_login = Column(TIMESTAMP, nullable=True)
    rol = relationship("Role", back_populates="usuarios")

    def __repr__(self):
        return f"<Usuario(id_usuario='{self.id_usuario}', num_documento='{self.num_documento}', password='{self.password}', id_rol='{self.id_rol}', estado='{self.estado}'), intentos_login='{self.intentos_login}', tiempo_de_fallo_login='{self.tiempo_de_fallo_login}')>"
    