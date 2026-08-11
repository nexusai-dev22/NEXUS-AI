"""
Definiciones oficiales de las memorias
que SYRAE puede almacenar.
"""

MEMORIAS = [

    {
        "clave": "proyecto_actual",

        "tipo": "proyecto",

        "descripcion": "Proyecto actual del usuario",

        "keywords": [
            "proyecto",
            "aplicación",
            "aplicacion",
            "sistema",
            "software",
            "programa",
        ],

        "patrones": [

            r"mi proyecto ahora se llama\s+(.+)",

            r"mi proyecto se llama\s+(.+)",

            r"mi proyecto es\s+(.+)",

            r"el proyecto se llama\s+(.+)",

            r"el nombre de mi proyecto es\s+(.+)",

            r"estoy desarrollando\s+(.+)",

            r"estoy creando\s+(.+)",

            r"trabajo en\s+(.+)",

            r"desarrollo\s+(.+)",

            r"mi aplicación se llama\s+(.+)",

            r"mi aplicacion se llama\s+(.+)",

            r"el sistema se llama\s+(.+)",

            r"estoy trabajando en\s+(.+)",
        ],
    },

    {
        "clave": "lenguaje_favorito",

        "tipo": "preferencia",

        "descripcion": "Lenguaje favorito",

        "keywords": [
            "python",
            "java",
            "php",
            "javascript",
            "typescript",
            "go",
            "rust",
            "c#",
            "c++",
        ],

        "patrones": [

            r"mi lenguaje favorito es\s+(.+)",

            r"mi lenguaje preferido es\s+(.+)",

            r"mi lenguaje principal es\s+(.+)",

            r"programo en\s+(.+)",

            r"mi lenguaje es\s+(.+)",

            r"desarrollo en\s+(.+)",

            r"uso\s+(.+)\s+como lenguaje principal",
        ],
    },

    {
        "clave": "intereses",

        "tipo": "preferencia",

        "descripcion": "Intereses del usuario",

        "keywords": [
            "gusta",
            "gustan",
            "interesa",
            "interesan",
            "apasiona",
            "apasionan",
            "encanta",
            "encantan",
            "interesado",
            "interesada",
        ],

        "patrones": [

            r"me gusta\s+(.+)",

            r"me gustan\s+(.+)",

            r"me interesa\s+(.+)",

            r"me interesan\s+(.+)",

            r"me apasiona\s+(.+)",

            r"me apasionan\s+(.+)",

            r"me encanta\s+(.+)",

            r"me encantan\s+(.+)",

            r"estoy interesado en\s+(.+)",

            r"estoy interesada en\s+(.+)",
        ],
    },
]
