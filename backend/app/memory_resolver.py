from sqlalchemy.orm import Session

from .memory import (
    obtener_memoria,
    obtener_memorias,
)

from .memory_questions import (
    PREGUNTAS_MEMORIA,
)


def resolver_desde_memoria(
    db: Session,
    usuario_id: int,
    mensaje: str,
):
    """
    Responde preguntas utilizando
    únicamente la memoria persistente.
    """

    texto = mensaje.lower().strip()

    # =====================================================
    # CONSULTAS ESPECÍFICAS
    # =====================================================

    for clave, preguntas in PREGUNTAS_MEMORIA.items():

        if any(
            pregunta in texto
            for pregunta in preguntas
        ):

            memoria = obtener_memoria(
                db=db,
                usuario_id=usuario_id,
                clave=clave,
            )

            if memoria:

                nombre = clave.replace(
                    "_",
                    " ",
                )

                nombre = nombre.capitalize()

                return (
                    f"{nombre}: "
                    f"{memoria.valor}."
                )

            return (
                "Todavía no tengo esa información "
                "almacenada en tu memoria."
            )

    # =====================================================
    # ¿QUÉ RECUERDAS DE MÍ?
    # =====================================================

    if (
        "qué recuerdas de mí" in texto
        or "que recuerdas de mi" in texto
    ):

        memorias = obtener_memorias(
            db=db,
            usuario_id=usuario_id,
        )

        if not memorias:

            return (
                "Todavía no tengo información "
                "almacenada sobre ti."
            )

        lineas = [
            "Esto es lo que recuerdo de ti:",
            "",
        ]

        for memoria in memorias:

            nombre = memoria.clave.replace(
                "_",
                " ",
            ).capitalize()

            lineas.append(
                f"- {nombre}: {memoria.valor}"
            )

        return "\n".join(lineas)

    return None
