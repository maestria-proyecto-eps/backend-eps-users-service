from sqlalchemy import Column, BigInteger, String, SmallInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base

class Farmaceuta(Base):
    __tablename__ = "farmaceutas"

    id_farmaceuta = Column(BigInteger, primary_key=True)
    nombres       = Column(String(50), nullable=False)
    apellidos     = Column(String(50), nullable=False)
    estado        = Column(SmallInteger, nullable=False)
    id_usuario    = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    usuario = relationship("Usuario", backref="farmaceutas")

    def __repr__(self):
        return f"<Farmaceuta(id={self.id_farmaceuta}, nombres={self.nombres})>"