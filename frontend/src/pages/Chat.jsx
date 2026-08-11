import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

import {
  crearConversacion,
  enviarMensaje,
  listarConversaciones,
  listarMensajes,
} from "../services/api";

function Chat() {
  const [searchParams] = useSearchParams();

  const [mensaje, setMensaje] = useState("");
  const [mensajes, setMensajes] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [cargandoChat, setCargandoChat] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    iniciarChat();
  }, [searchParams]);

  async function iniciarChat() {
    try {
      setError("");
      setCargandoChat(true);

      const idSeleccionado =
        searchParams.get("conversation");

      const conversaciones =
        await listarConversaciones();

      let conversacion;

      if (idSeleccionado) {
        conversacion = conversaciones.find(
          (item) =>
            item.id === Number(idSeleccionado)
        );

        if (!conversacion) {
          throw new Error(
            "La conversación seleccionada no existe."
          );
        }
      } else if (conversaciones.length > 0) {
        conversacion = conversaciones.reduce(
          (ultima, actual) =>
            actual.id > ultima.id
              ? actual
              : ultima
        );
      } else {
        conversacion =
          await crearConversacion(
            "Nueva conversación"
          );
      }

      setConversationId(conversacion.id);

      const historial =
        await listarMensajes(
          conversacion.id
        );

      if (historial.length > 0) {
        setMensajes(
          historial.map((item) => ({
            tipo:
              item.rol === "user"
                ? "usuario"
                : "ia",
            texto: item.contenido,
          }))
        );
      } else {
        setMensajes([
          {
            tipo: "ia",
            texto:
              "Hola. Soy SYRAE, la inteligencia de VAYRONA. ¿En qué puedo ayudarte hoy?",
          },
        ]);
      }
    } catch (error) {
      console.error(error);

      setError(
        error.message ||
          "No se pudo cargar la conversación."
      );
    } finally {
      setCargandoChat(false);
    }
  }

  async function enviar() {
    if (
      !mensaje.trim() ||
      cargando ||
      !conversationId
    ) {
      return;
    }

    const textoUsuario = mensaje.trim();

    setMensaje("");
    setError("");

    setMensajes((anteriores) => [
      ...anteriores,
      {
        tipo: "usuario",
        texto: textoUsuario,
      },
    ]);

    setCargando(true);

    try {
      const respuesta =
        await enviarMensaje(
          conversationId,
          "user",
          textoUsuario
        );

      setCargando(false);

      const contenido =
        respuesta?.respuesta?.contenido ||
        respuesta?.contenido ||
        "SYRAE recibió tu mensaje.";

      setMensajes((anteriores) => [
        ...anteriores,
        {
          tipo: "ia",
          texto: contenido,
        },
      ]);
    } catch (error) {
      console.error(error);

      setCargando(false);

      setError(
        error.message ||
          "No se pudo enviar el mensaje."
      );
    }
  }

  if (cargandoChat) {
    return (
      <div className="chat-loading">
        Cargando conversación...
      </div>
    );
  }

  return (
    <div className="chat-page">

      <header className="chat-header">
        <div>
          <h1>SYRAE</h1>

          <p>
            Conversación #{conversationId}
          </p>
        </div>

        <div className="estado">
          <span className="estado-punto"></span>
          Online
        </div>
      </header>

      {error && (
        <div className="chat-error">
          {error}
        </div>
      )}

      <div className="chat-container">

        {mensajes.map((item, index) => (
          <div
            key={index}
            className={`mensaje ${item.tipo}`}
          >
            {item.tipo === "ia" && (
              <div className="mensaje-avatar">
                S
              </div>
            )}

            <div className="mensaje-contenido">
              <strong>
                {item.tipo === "ia"
                  ? "SYRAE"
                  : "Tú"}
              </strong>

              <p>{item.texto}</p>
            </div>
          </div>
        ))}

        {cargando && (
          <div className="mensaje ia">
            <div className="mensaje-avatar">
              S
            </div>

            <div className="mensaje-contenido">
              <strong>SYRAE</strong>

              <p>Pensando...</p>
            </div>
          </div>
        )}

      </div>

      <div className="chat-input-container">

        <input
          type="text"
          placeholder="Escribe un mensaje..."
          value={mensaje}
          onChange={(e) =>
            setMensaje(e.target.value)
          }
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              enviar();
            }
          }}
          disabled={
            cargando ||
            !conversationId
          }
        />

        <button
          onClick={enviar}
          disabled={
            cargando ||
            !conversationId
          }
        >
          {cargando
            ? "Enviando..."
            : "Enviar"}
        </button>

      </div>

    </div>
  );
}

export default Chat;
