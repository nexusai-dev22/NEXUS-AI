from sqlalchemy.orm import Session

from .memory import guardar_memoria
from .nlp_engine import detectar_memoria


def extraer_memoria_generica(
    db: Session,
    usuario_id: int,
    texto: str,
):
    """
    Utiliza el motor NLP para detectar
    información relevante y almacenarla.
    """

    memoria = detectar_memoria(texto)

    if memoria is None:
        return False

    guardar_memoria(
        db=db,
        usuario_id=usuario_id,
        tipo=memoria["tipo"],
        clave=memoria["clave"],
        valor=memoria["valor"],
    )

    print(
        f"[MEMORY] {memoria['clave']} = {memoria['valor']}"
    )

    return True


# ==========================================================
# COMPATIBILIDAD
# ==========================================================

def extraer_proyecto(
    db: Session,
    usuario_id: int,
    texto: str,
):
    return extraer_memoria_generica(
        db=db,
        usuario_id=usuario_id,
        texto=texto,
    )


def extraer_lenguaje(
    db: Session,
    usuario_id: int,
    texto: str,
):
    return extraer_memoria_generica(
        db=db,
        usuario_id=usuario_id,
        texto=texto,
    )
