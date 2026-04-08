from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from database import engine, Base, SessionLocal
import models
from models import Usuario, Post
from schemas import UsuarioCreate, UsuarioResponse, UsuarioUpdate, PostResponse, PostCreate, LoginRequest, PostUpdate
from sqlalchemy.orm import Session
from security import verify_password, create_access_token, hash_password, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

#Crear las tablas en la base de datos 
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return{"mensaje": "Api funcionando correctamente"}

@app.post("/usuarios/", response_model=UsuarioResponse)
def crear_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
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

@app.get("/usuarios/", response_model=list[UsuarioResponse])
def obtener_usuarios(db: Session =
Depends(get_db)):   
    usuarios = db.query(Usuario).all()
    return usuarios

@app.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, db:
Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
     
    return usuario 

@app.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate, db:
Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if usuario_db is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    
    if usuario.username is not None:
        usuario_db.username = usuario.username

    if usuario.email is not None:
        usuario_db.email = usuario.email

    if usuario.edad is not None:
        usuario_db.edad = usuario.edad
    
    db.commit()
    db.refresh(usuario_db)
    
    return usuario_db

@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, db:
Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if usuario_db is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    
    db.delete(usuario_db)
    db.commit()

    return {"mensaje": "Usuario eliminado"}

# Un usaurio muchos posts

@app.get("/usuarios/{usuario_id}/posts", response_model=list[PostResponse])
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
    
    posts = db.query(Post).filter(Post.usuario_id == usuario_id).offset(offset).limit(limit).all()

    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def crear_post(post: PostCreate, db:
Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):

    nuevo_post = Post(
        titulo = post.titulo,
        contenido = post.contenido,
        usuario_id = current_user.id
    )

    db.add(nuevo_post)
    db.commit()
    db.refresh(nuevo_post)

    return nuevo_post

@app.delete("/posts/{post_id}")
def eliminar_post(post_id: int, db:
Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
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

    return{"mensaje": "Post eliminado correctamente"}

@app.put("/posts/{post_id}")
def actualizar_post(post_id: int, post: PostUpdate, db:
Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
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

    return{"mensaje": "Post actulizado correctamente"}

@app.get("/posts", response_model=list[PostResponse])
def obtener_mis_post(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    search: str = None
):
   posts_db = db.query(Post).filter(Post.usuario_id == current_user.id).filter(Post.titulo.contains(search)).order_by(Post.id.desc()).offset(offset).limit(limit)

   return posts_db

# Login Schema

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db:
Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.username == form_data.username).first()

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )
    
    if not verify_password(form_data.password,
    usuario.password):
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )
    
    token_data = {
        "sub": usuario.id
    }

    access_token = create_access_token(token_data)

    return{
        "access_token": access_token,
        "token_type": "bearer"
    }

