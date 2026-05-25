from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from database import get_db
from models import Usuario
from schemas import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from security import hash_password

router = APIRouter()


@router.post("/usuarios/", response_model=UsuarioResponse)
def crear_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    duplicate_filters = [Usuario.username == usuario.username]

    if usuario.email is not None:
        duplicate_filters.append(Usuario.email == usuario.email)

    usuario_existente = (
        db.query(Usuario)
        .filter(or_(*duplicate_filters))
        .first()
    )

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="Username o email ya registrado"
        )

    hashed_password = hash_password(usuario.password)

    nuevo_usuario = Usuario(
        username=usuario.username,
        email=usuario.email,
        edad=usuario.edad,
        password=hashed_password
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


@router.get("/usuarios/", response_model=list[UsuarioResponse])
def obtener_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return usuarios


@router.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario


@router.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(
    usuario_id: int,
    usuario: UsuarioUpdate,
    db: Session = Depends(get_db)
):
    usuario_db = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if usuario_db is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if usuario.username is not None:
        username_existente = (
            db.query(Usuario)
            .filter(Usuario.username == usuario.username, Usuario.id != usuario_id)
            .first()
        )

        if username_existente:
            raise HTTPException(
                status_code=400,
                detail="Username ya registrado"
            )

        usuario_db.username = usuario.username

    if usuario.email is not None:
        email_existente = (
            db.query(Usuario)
            .filter(Usuario.email == usuario.email, Usuario.id != usuario_id)
            .first()
        )

        if email_existente:
            raise HTTPException(
                status_code=400,
                detail="Email ya registrado"
            )

        usuario_db.email = usuario.email

    if usuario.edad is not None:
        usuario_db.edad = usuario.edad

    db.commit()
    db.refresh(usuario_db)

    return usuario_db


@router.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if usuario_db is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    db.delete(usuario_db)
    db.commit()

    return {"mensaje": "Usuario eliminado"}
