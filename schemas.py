from pydantic import BaseModel, Field
from typing import Optional

class UsuarioCreate(BaseModel):
    username: str = Field(min_length=1)
    email: Optional[str] = None
    edad: int = Field(ge=0)
    password: str = Field(min_length=1)

class UsuarioResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    edad: int

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=1)
    email: Optional[str] = None
    edad: Optional[int] = Field(default=None, ge=0)


class PostCreate(BaseModel):
    titulo: str = Field(min_length=1)
    contenido: str = Field(min_length=1)

class PostResponse(BaseModel):
    id: int
    titulo: str
    contenido: str
    usuario: UsuarioResponse

    class Config:
        from_attributes = True

class PostSimpleResponse(BaseModel):
    id: int
    titulo: str
    contenido: str

    class Config:
        from_attributes = True

class PostUpdate(BaseModel):
    titulo: Optional[str] = Field(default=None, min_length=1)
    contenido: Optional[str] = Field(default=None, min_length=1)

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
