from sqlalchemy.orm import Session

from .models import Memory


def guardar_memoria(
    db: Session,
    usuario_id: int,
    tipo: str,
    clave: str,
    valor: str,
):
    """
    Guarda o actualiza una memoria del usuario.
    """

    memoria = (
        db.query(Memory)
        .filter(
            Memory.usuario_id == usuario_id,
            Memory.clave == clave,
        )
        .first()
    )

    if memoria:
        memoria.tipo = tipo
        memoria.valor = valor
    else:
        memoria = Memory(
            usuario_id=usuario_id,
            tipo=tipo,
            clave=clave,
            valor=valor,
        )

        db.add(memoria)

    db.commit()
    db.refresh(memoria)

    return memoria


def obtener_memorias(
    db: Session,
    usuario_id: int,
):
    """
    Obtiene todas las memorias del usuario.
    """

    return (
        db.query(Memory)
        .filter(
            Memory.usuario_id == usuario_id,
        )
        .order_by(
            Memory.actualizado_en.desc()
        )
        .all()
    )


def obtener_memoria(
    db: Session,
    usuario_id: int,
    clave: str,
):
    """
    Obtiene una memoria específica.
    """

    return (
        db.query(Memory)
        .filter(
            Memory.usuario_id == usuario_id,
            Memory.clave == clave,
        )
        .first()
    )


def eliminar_memoria(
    db: Session,
    usuario_id: int,
    clave: str,
):
    """
    Elimina una memoria específica.
    """

    memoria = (
        db.query(Memory)
        .filter(
            Memory.usuario_id == usuario_id,
            Memory.clave == clave,
        )
        .first()
    )

    if not memoria:
        return False

    db.delete(memoria)
    db.commit()

    return True


def construir_contexto_memoria(
    db: Session,
    usuario_id: int,
):
    """
    Convierte las memorias del usuario
    en un contexto que SYRAE pueda utilizar.
    """

    memorias = obtener_memorias(
        db,
        usuario_id,
    )

    if not memorias:
        return ""

    lineas = [
        "MEMORIA DEL USUARIO:",
        "",
    ]

    for memoria in memorias:
        lineas.append(
            f"- {memoria.clave}: {memoria.valor}"
        )

    return "\n".join(lineas)


def guardar_memoria_proyecto(
    db: Session,
    usuario_id: int,
    proyecto: str,
):
    """
    Guarda o actualiza el proyecto actual del usuario.
    """

    return guardar_memoria(
        db=db,
        usuario_id=usuario_id,
        tipo="proyecto",
        clave="proyecto_actual",
        valor=proyecto,
    )


def obtener_proyecto_actual(
    db: Session,
    usuario_id: int,
):
    """
    Obtiene el proyecto actual del usuario.
    """

    memoria = obtener_memoria(
        db=db,
        usuario_id=usuario_id,
        clave="proyecto_actual",
    )

    if not memoria:
        return None

    return memoria.valor
import re


def detectar_y_guardar_memoria(
    db: Session,
    usuario_id: int,
    texto: str,
):
    """
    Detecta información que el usuario está proporcionando
    explícitamente y la guarda en la memoria persistente.
    """

    texto = texto.strip()

    patrones_proyecto = [
        r"mi proyecto ahora se llama\s+(.+)",
        r"mi proyecto se llama\s+(.+)",
        r"el proyecto ahora se llama\s+(.+)",
        r"el proyecto se llama\s+(.+)",
        r"mi proyecto es\s+(.+)",
        r"el nombre de mi proyecto es\s+(.+)",
    ]

    for patron in patrones_proyecto:

        coincidencia = re.search(
            patron,
            texto,
            re.IGNORECASE,
        )

        if coincidencia:

            proyecto = coincidencia.group(1).strip()

            proyecto = re.sub(
                r"[.!?,]+$",
                "",
                proyecto,
            ).strip()

            if not proyecto:
                return None

            return guardar_memoria(
                db=db,
                usuario_id=usuario_id,
                tipo="proyecto",
                clave="proyecto_actual",
                valor=proyecto,
            )

    return None
