from .memory_extractors import (
    extraer_proyecto,
    extraer_lenguaje,
)

# ==========================================================
# REGISTRO DE EXTRACTORES
# ==========================================================

EXTRACTORES = [
    extraer_proyecto,
    extraer_lenguaje,
]
