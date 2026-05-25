from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Post, Usuario
from schemas import PostCreate, PostResponse, PostSimpleResponse, PostUpdate
from security import get_current_user

router = APIRouter()


@router.get("/usuarios/{usuario_id}/posts", response_model=list[PostSimpleResponse])
def obterner_posts_usuario(
    usuario_id: int,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    usuario_db = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if usuario_db is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if current_user.id != usuario_id:
        raise HTTPException(
            status_code=403,
            detail="No autorizado"
        )

    posts = db.query(Post).filter(Post.usuario_id == usuario_id).offset(offset).limit(limit).all()

    return posts


@router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def crear_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    nuevo_post = Post(
        titulo=post.titulo,
        contenido=post.contenido,
        usuario_id=current_user.id
    )

    db.add(nuevo_post)
    db.commit()
    db.refresh(nuevo_post)

    return nuevo_post


@router.delete("/posts/{post_id}")
def eliminar_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    post_db = db.query(Post).filter(Post.id == post_id).first()

    if post_db is None:
        raise HTTPException(
            status_code=404,
            detail="Post no encontrado"
        )
    if post_db.usuario_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="No autorizado"
        )

    db.delete(post_db)
    db.commit()

    return {"mensaje": "Post eliminado correctamente"}


@router.put("/posts/{post_id}", response_model=PostResponse)
def actualizar_post(
    post_id: int,
    post: PostUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    post_db = db.query(Post).filter(Post.id == post_id).first()

    if post_db is None:
        raise HTTPException(
            status_code=404,
            detail="Post no encontrado"
        )
    if post_db.usuario_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="No autorizado"
        )

    if post.titulo is not None:
        post_db.titulo = post.titulo

    if post.contenido is not None:
        post_db.contenido = post.contenido

    db.commit()
    db.refresh(post_db)

    return post_db


@router.get("/posts", response_model=list[PostResponse])
def obtener_mis_post(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    search: str = ""
):
    query = db.query(Post).filter(Post.usuario_id == current_user.id)

    if search:
        query = query.filter(Post.titulo.contains(search))

    posts_db = query.order_by(Post.id.desc()).offset(offset).limit(limit).all()

    return posts_db
