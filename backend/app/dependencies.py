from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .database import get_db
from .models import User
from .routers.auth import SECRET_KEY, ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credenciales_invalidas = HTTPException(
        status_code=401,
        detail="Token inválido o expirado",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )

    try:
        datos = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        usuario_id = datos.get("sub")

        if usuario_id is None:
            raise credenciales_invalidas

    except JWTError:
        raise credenciales_invalidas

    usuario = (
        db.query(User)
        .filter(User.id == int(usuario_id))
        .first()
    )

    if usuario is None:
        raise credenciales_invalidas

    return usuario
