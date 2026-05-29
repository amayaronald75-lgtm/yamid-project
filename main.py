from fastapi import FastAPI

from database import Base, engine
from routers import auth, posts, users

app = FastAPI()

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)


@app.get("/")
def read_root():
    return {"mensaje": "Api funcionando correctamente"}
