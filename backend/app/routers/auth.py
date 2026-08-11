from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from jose import jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..auth import crear_hash_password, verificar_password
from ..database import get_db
from ..models import User

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"],
)


SECRET_KEY = "CAMBIAR_ESTA_CLAVE_POR_UNA_MUY_SEGURA"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


class RegistroRequest(BaseModel):
    nombre: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def registrar_usuario(
    datos: RegistroRequest,
    db: Session = Depends(get_db),
):
    usuario_existente = (
        db.query(User)
        .filter(User.email == datos.email)
        .first()
    )

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="El correo electrónico ya está registrado",
        )

    nuevo_usuario = User(
        nombre=datos.nombre,
        email=datos.email,
        password_hash=crear_hash_password(datos.password),
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {
        "mensaje": "Usuario registrado correctamente",
        "usuario": {
            "id": nuevo_usuario.id,
            "nombre": nuevo_usuario.nombre,
            "email": nuevo_usuario.email,
        },
    }

@router.post("/login")
def iniciar_sesion(
    datos: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    usuario = (
        db.query(User)
        .filter(User.email == datos.username)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos",
        )

    if not verificar_password(
        datos.password,
        usuario.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos",
        )

    ahora = datetime.now(timezone.utc)

    expiracion = ahora + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    token = jwt.encode(
        {
            "sub": str(usuario.id),
            "exp": expiracion,
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
        },
    }
