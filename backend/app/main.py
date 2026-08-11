from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .dependencies import obtener_usuario_actual
from .database import Base, engine
from . import models
from .routers.auth import router as auth_router
from .routers.conversations import router as conversations_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="VAYRONA API",
    version="0.1.0",
)

app.include_router(conversations_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a VAYRONA 🚀"
    }


@app.get("/status")
def status():
    return {
        "estado": "Servidor funcionando"
    }


@app.post("/chat")
def chat(
    datos: dict,
    usuario=Depends(obtener_usuario_actual),
):
    mensaje = datos.get("mensaje", "")

    return {
        "respuesta": (
            f"Hola {usuario.nombre}. "
            f"SYRAE recibió tu mensaje: {mensaje}"
        )
    }
