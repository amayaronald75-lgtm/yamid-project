from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    edad = Column(Integer)
    password = Column(String)
    posts = relationship("Post", back_populates="usuario")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, unique=True, index=True)
    contenido = Column(String)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), index=True)
    usuario = relationship("Usuario", back_populates="posts")

