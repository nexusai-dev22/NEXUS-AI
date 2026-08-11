"""
Motor NLP de SYRAE.

Este módulo detecta información relevante
utilizando las definiciones oficiales
de memoria.

En futuras versiones podrá sustituirse
por spaCy, embeddings o un LLM sin cambiar
el resto del backend.
"""

import re

from .memory_definitions import MEMORIAS


def _limpiar(texto: str) -> str:
    texto = texto.strip()

    texto = re.sub(
        r"[.!?,]+$",
        "",
        texto,
    )

    return texto.strip()


def detectar_memoria(texto: str):
    """
    Devuelve una memoria detectada o None.

    Formato:

    {
        "clave": "...",
        "tipo": "...",
        "valor": "...",
        "intencion": "..."
    }
    """

    texto_original = texto

    texto = texto.lower().strip()

    for memoria in MEMORIAS:

        # ---------------------------------------
        # FILTRO POR PALABRAS CLAVE
        # ---------------------------------------

        if memoria.get("keywords"):

            if not any(
                keyword.lower() in texto
                for keyword in memoria["keywords"]
            ):
                continue

        # ---------------------------------------
        # PATRONES
        # ---------------------------------------

        for patron in memoria["patrones"]:

            coincidencia = re.search(
                patron,
                texto_original,
                re.IGNORECASE,
            )

            if not coincidencia:
                continue

            valor = _limpiar(
                coincidencia.group(1)
            )

            if not valor:
                continue

            return {

                "clave": memoria["clave"],

                "tipo": memoria["tipo"],

                "valor": valor,

                "intencion": "guardar_memoria",

            }

    return None
