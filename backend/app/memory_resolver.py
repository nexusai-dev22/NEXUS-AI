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
    # NOMBRE DEL USUARIO
    # =====================================================

    preguntas_nombre = [
        "cuál es mi nombre",
        "cual es mi nombre",
        "cómo me llamo",
        "como me llamo",
        "dime mi nombre",
        "dime como me llamo",
    ]

    if any(
        pregunta in texto
        for pregunta in preguntas_nombre
    ):

        from .models import User

        usuario = (
            db.query(User)
            .filter(User.id == usuario_id)
            .first()
        )

        if usuario and usuario.nombre:
            return f"Tu nombre es {usuario.nombre}."

        return (
            "Todavía no tengo registrado "
            "tu nombre."
        )

    # =====================================================
    # CONSULTAS ESPECÍFICAS DE MEMORIA
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

    preguntas_recuerdo = [
        "qué recuerdas de mí",
        "que recuerdas de mi",
        "qué sabes de mí",
        "que sabes de mi",
        "qué recuerdas sobre mí",
        "que recuerdas sobre mi",
        "qué sabes sobre mí",
        "que sabes sobre mi",
    ]

    if any(
        pregunta in texto
        for pregunta in preguntas_recuerdo
    ):

        from .models import User

        usuario = (
            db.query(User)
            .filter(User.id == usuario_id)
            .first()
        )

        memorias = obtener_memorias(
            db=db,
            usuario_id=usuario_id,
        )

        lineas = [
            "Esto es lo que recuerdo de ti:",
            "",
        ]

        if usuario and usuario.nombre:
            lineas.append(
                f"- Nombre: {usuario.nombre}"
            )

        for memoria in memorias:

            nombre = memoria.clave.replace(
                "_",
                " ",
            ).capitalize()

            lineas.append(
                f"- {nombre}: {memoria.valor}"
            )

        if len(lineas) == 2:
            return (
                "Todavía no tengo información "
                "almacenada sobre ti."
            )

        return "\n".join(lineas)

    return None
