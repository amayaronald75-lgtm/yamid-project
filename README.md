# yamid-project

API desarrollada con FastAPI para la gestión de usuarios y posts, incluyendo autenticación con JWT, hash de contraseñas y operaciones CRUD sobre los recursos principales.

## 🚀 Características

- Registro de usuarios
- Inicio de sesión con token JWT
- Hash seguro de contraseñas con `bcrypt`
- CRUD de usuarios
- Creación, actualización, eliminación y consulta de posts
- Protección de rutas mediante autenticación
- Base de datos SQLite con SQLAlchemy ORM

## 🛠️ Tecnologías usadas

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Passlib
- Python-Jose

## 🧩 Estructura del proyecto

```text
backend_project/
├── main.py
├── models.py
├── schemas.py
├── security.py
├── database.py
├── usuarios.db
└── README.md
```

## 🔧 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/amayaronald75-lgtm/yamid-project.git
cd yamid-project/backend_project
```

2. Crea y activa un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate
```

En Windows:

```bash
venv\Scripts\activate
```

3. Instala las dependencias:

```bash
pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose python-multipart
```

## ⚙️ Ejecución

Inicia el servidor con:

```bash
uvicorn main:app --reload
```

Luego abre en el navegador:

- Documentación Swagger: `http://127.0.0.1:8000/docs`
- Documentación Redoc: `http://127.0.0.1:8000/redoc`

## ✅ Autenticación

El proyecto utiliza JWT para proteger rutas.

### 🔀 Flujo básico

1. Crear un usuario en `POST /usuarios/`
2. Iniciar sesión en `POST /login`
3. Copiar el `access_token`
4. Usar el token en rutas protegidas con el esquema:

```text
Authorization: Bearer tu_token
```

## 📡 Endpoints principales

### Usuarios

- `POST /usuarios/` Crear usuario
- `GET /usuarios/` Obtener todos los usuarios
- `GET /usuarios/{usuario_id}` Obtener un usuario por ID
- `PUT /usuarios/{usuario_id}` Actualizar usuario
- `DELETE /usuarios/{usuario_id}` Eliminar usuario
- `GET /usuarios/{usuario_id}/posts` Obtener los posts de un usuario autenticado

### Autenticación

- `POST /login` Iniciar sesión y obtener token

### Posts

- `POST /posts` Crear un post
- `GET /posts` Obtener los posts del usuario autenticado
- `PUT /posts/{post_id}` Actualizar un post
- `DELETE /posts/{post_id}` Eliminar un post

## 🗂️ Modelos principales

### Usuario

- `id`
- `username`
- `email`
- `edad`
- `password`

### Post

- `id`
- `titulo`
- `contenido`
- `usuario_id`

## 📌 Estado del proyecto

El proyecto cuenta con autenticación, manejo de usuarios y operaciones sobre posts. Puede seguir ampliándose con mejoras como validaciones más estrictas, manejo de errores más robusto y separación por routers.

## 👨‍💻 Autor

Desarrollado por `amayaronald75-lgtm`.
