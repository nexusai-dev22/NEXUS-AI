from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ollama import chat

from ..database import get_db
from ..dependencies import obtener_usuario_actual
from ..models import Conversation, Message, User
from ..vayrona_context import VAYRONA_CONTEXT
from ..memory import (
    construir_contexto_memoria,
)

from ..memory_manager import (
    procesar_memoria,
)

router = APIRouter(
    prefix="/conversations",
    tags=["Conversaciones"],
)


# ============================================================
# MODELOS DE PETICIÓN
# ============================================================

class CrearConversacionRequest(BaseModel):
    titulo: str = "Nueva conversación"


class CrearMensajeRequest(BaseModel):
    rol: str
    contenido: str


# ============================================================
# CREAR CONVERSACIÓN
# ============================================================

@router.post("")
def crear_conversacion(
    datos: CrearConversacionRequest,
    usuario: User = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db),
):
    conversacion = Conversation(
        usuario_id=usuario.id,
        titulo=datos.titulo,
    )

    db.add(conversacion)
    db.commit()
    db.refresh(conversacion)

    return {
        "id": conversacion.id,
        "titulo": conversacion.titulo,
        "usuario_id": conversacion.usuario_id,
        "creado_en": conversacion.creado_en,
    }


# ============================================================
# LISTAR CONVERSACIONES
# ============================================================

@router.get("")
def listar_conversaciones(
    usuario: User = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db),
):
    return (
        db.query(Conversation)
        .filter(
            Conversation.usuario_id == usuario.id
        )
        .order_by(
            Conversation.creado_en.desc()
        )
        .all()
    )


# ============================================================
# AGREGAR MENSAJE
# ============================================================

@router.post("/{conversation_id}/messages")
def agregar_mensaje(
    conversation_id: int,
    datos: CrearMensajeRequest,
    usuario: User = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db),
):

    # ========================================================
    # 1. VERIFICAR CONVERSACIÓN
    # ========================================================

    conversacion = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.usuario_id == usuario.id,
        )
        .first()
    )

    if not conversacion:
        raise HTTPException(
            status_code=404,
            detail="Conversación no encontrada",
        )

    # ========================================================
    # 2. GUARDAR MENSAJE DEL USUARIO
    # ========================================================

    mensaje_usuario = Message(
        conversation_id=conversation_id,
        rol="user",
        contenido=datos.contenido,
    )

    db.add(mensaje_usuario)
    db.commit()
    db.refresh(mensaje_usuario)

    # ========================================================
    # 3. DETECTAR Y GUARDAR MEMORIA AUTOMÁTICAMENTE
    # ========================================================

    respuesta_memoria = procesar_memoria(
        db=db,
        usuario_id=usuario.id,
        mensaje=datos.contenido,
    )

    if respuesta_memoria:

        mensaje_ia = Message(
            conversation_id=conversation_id,
            rol="assistant",
            contenido=respuesta_memoria,
        )

        db.add(mensaje_ia)
        db.commit()
        db.refresh(mensaje_ia)

        return {
            "mensaje_usuario": {
                "id": mensaje_usuario.id,
                "conversation_id": mensaje_usuario.conversation_id,
                "rol": mensaje_usuario.rol,
                "contenido": mensaje_usuario.contenido,
                "creado_en": mensaje_usuario.creado_en,
            },
            "respuesta": {
                "id": mensaje_ia.id,
                "conversation_id": mensaje_ia.conversation_id,
                "rol": mensaje_ia.rol,
                "contenido": mensaje_ia.contenido,
                "creado_en": mensaje_ia.creado_en,
            },
        }
    # ========================================================
    # 4. OBTENER HISTORIAL COMPLETO
    # ========================================================

    historial = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id
        )
        .order_by(
            Message.creado_en.asc()
        )
        .all()
    )

    # ========================================================
    # 5. OBTENER MEMORIA ACTUALIZADA
    # ========================================================

    contexto_memoria = construir_contexto_memoria(
        db,
        usuario.id,
    )

    # ========================================================
    # 6. CONSTRUIR CONTEXTO OFICIAL DE VAYRONA
    # ========================================================

    contexto_sistema = VAYRONA_CONTEXT

    contexto_sistema += """

REGLAS DE CONTEXTO DEL SISTEMA:

La información que aparece a continuación ha sido
proporcionada directamente por el sistema VAYRONA.

Debes utilizarla cuando sea relevante para responder
al usuario.

Si el sistema proporciona un dato sobre el usuario,
puedes utilizar ese dato directamente.

No digas que no tienes acceso a un dato si ese dato
aparece en la MEMORIA DEL USUARIO.

No contradigas información proporcionada directamente
por el sistema.

Si una información no aparece en el contexto oficial
ni en la memoria proporcionada por el sistema,
indica honestamente que no tienes información sobre ella.

"""

    # ========================================================
    # 7. AGREGAR MEMORIA
    # ========================================================

    if contexto_memoria:
        contexto_sistema += "\n\n"
        contexto_sistema += contexto_memoria

    # ========================================================
    # 8. AGREGAR IDENTIDAD DEL USUARIO
    # ========================================================

    contexto_sistema += f"""

DATOS BÁSICOS DEL USUARIO:

Nombre:
{usuario.nombre}

El usuario actualmente está interactuando con VAYRONA
a través del asistente SYRAE.

"""

    # ========================================================
    # 9. CONSTRUIR MENSAJES PARA OLLAMA
    # ========================================================

    messages = [
        {
            "role": "system",
            "content": contexto_sistema,
        }
    ]

    for mensaje in historial:

        if mensaje.rol in (
            "user",
            "assistant",
        ):
            messages.append(
                {
                    "role": mensaje.rol,
                    "content": mensaje.contenido,
                }
            )

    # ========================================================
    # 10. CONSULTAR SYRAE
    # ========================================================

    try:

        print(
            f"[SYRAE] Usuario: {usuario.id}"
        )

        print(
            f"[SYRAE] Conversación: {conversation_id}"
        )

        print(
            f"[SYRAE] Mensajes enviados: {len(messages)}"
        )

        print(
            "\n========== MEMORIA UTILIZADA =========="
        )

        if contexto_memoria:
            print(contexto_memoria)
        else:
            print("No hay memoria almacenada.")

        print(
            "========== FIN MEMORIA ==========\n"
        )

        print(
            "\n========== CONTEXTO ENVIADO A SYRAE =========="
        )

        print(contexto_sistema)


        print(
            "========== FIN CONTEXTO ==========\n"
        )

        print(
            "\n========== MENSAJES ENVIADOS ==========\n"
        )

        for i, mensaje in enumerate(messages):

            print(f"\n----- MENSAJE {i} -----")
            print("ROLE:", mensaje["role"])
            print(mensaje["content"])

        print(
            "\n========== FIN MENSAJES ==========\n"
        )

        respuesta_ia = chat(
            model="syrae-memory",
            messages=messages,
            options={
                "num_predict": 256,
                "temperature": 0.3,
            },
        )

        texto_respuesta = (
            respuesta_ia.message.content
            or "No pude generar una respuesta."
        )

        print(
            "[SYRAE] Respuesta generada correctamente."
        )

    except Exception as error:

        print(
            "[ERROR OLLAMA SYRAE]:",
            repr(error),
        )

        raise HTTPException(
            status_code=500,
            detail="No se pudo obtener respuesta de SYRAE.",
        )

    # ========================================================
    # 11. GUARDAR RESPUESTA DE SYRAE
    # ========================================================

    mensaje_ia = Message(
        conversation_id=conversation_id,
        rol="assistant",
        contenido=texto_respuesta,
    )

    db.add(mensaje_ia)
    db.commit()
    db.refresh(mensaje_ia)

    # ========================================================
    # 12. RESPUESTA AL FRONTEND
    # ========================================================

    return {
        "mensaje_usuario": {
            "id": mensaje_usuario.id,
            "conversation_id": mensaje_usuario.conversation_id,
            "rol": mensaje_usuario.rol,
            "contenido": mensaje_usuario.contenido,
            "creado_en": mensaje_usuario.creado_en,
        },
        "respuesta": {
            "id": mensaje_ia.id,
            "conversation_id": mensaje_ia.conversation_id,
            "rol": mensaje_ia.rol,
            "contenido": mensaje_ia.contenido,
            "creado_en": mensaje_ia.creado_en,
        },
    }


# ============================================================
# LISTAR MENSAJES
# ============================================================

@router.get("/{conversation_id}/messages")
def listar_mensajes(
    conversation_id: int,
    usuario: User = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db),
):

    conversacion = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.usuario_id == usuario.id,
        )
        .first()
    )

    if not conversacion:
        raise HTTPException(
            status_code=404,
            detail="Conversación no encontrada",
        )

    return (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id
        )
        .order_by(
            Message.creado_en.asc()
        )
        .all()
    )
