from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Usuario
from routers import posts, users
from schemas import TokenResponse
from security import create_access_token, verify_password

app = FastAPI()

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(posts.router)


@app.get("/")
def read_root():
    return {"mensaje": "Api funcionando correctamente"}


@app.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.username == form_data.username).first()

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    if not verify_password(form_data.password, usuario.password):
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    token_data = {
        "sub": str(usuario.id)
    }

    access_token = create_access_token(token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
