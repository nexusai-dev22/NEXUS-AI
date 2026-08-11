from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class MemoryRecord:
    """
    Representa una memoria enriquecida.

    Esta clase prepara el sistema para
    futuras versiones sin modificar
    el resto del backend.
    """

    clave: str

    tipo: str

    valor: str

    confianza: float = 1.0

    origen: str = "usuario"

    version: int = 1

    actualizado: Optional[datetime] = None

    def to_dict(self):

        return {

            "clave": self.clave,

            "tipo": self.tipo,

            "valor": self.valor,

            "confianza": self.confianza,

            "origen": self.origen,

            "version": self.version,

            "actualizado": self.actualizado,

        }
