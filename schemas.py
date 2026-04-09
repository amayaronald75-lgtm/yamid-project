from pydantic import BaseModel
from typing import Optional

class UsuarioCreate(BaseModel):
    username: str
    email: Optional[str] = None
    edad: int
    password: str

class UsuarioResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    edad: int
    posts: list["PostResponse"]

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    edad: Optional[int] = None


class PostCreate(BaseModel):
    titulo: str
    contenido: str

class PostResponse(BaseModel):
    id: int
    titulo: str
    contenido: str
    usuario: UsuarioResponse

class PostUpdate(BaseModel):
    titulo: Optional[str] = None
    contenido: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str
