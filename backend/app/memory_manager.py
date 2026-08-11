from sqlalchemy.orm import Session

from .memory_registry import EXTRACTORES
from .memory_resolver_registry import RESOLVERS


def procesar_memoria(
    db: Session,
    usuario_id: int,
    mensaje: str,
):
    """
    Procesa la memoria del usuario.

    Flujo:

    1. Ejecuta todos los extractores registrados.
    2. Si alguno detecta una memoria, la almacena.
    3. Ejecuta todos los resolvers registrados.
    4. Devuelve la primera respuesta encontrada.
    """

    # =====================================================
    # EXTRACTORES
    # =====================================================

    for extractor in EXTRACTORES:

        try:

            extractor(
                db=db,
                usuario_id=usuario_id,
                texto=mensaje,
            )

        except Exception as error:

            print(
                f"[MEMORY][Extractor] "
                f"{extractor.__name__}: "
                f"{error}"
            )

    # =====================================================
    # RESOLVERS
    # =====================================================

    for resolver in RESOLVERS:

        try:

            respuesta = resolver(
                db=db,
                usuario_id=usuario_id,
                mensaje=mensaje,
            )

            if respuesta:
                return respuesta

        except Exception as error:

            print(
                f"[MEMORY][Resolver] "
                f"{resolver.__name__}: "
                f"{error}"
            )

    return None
