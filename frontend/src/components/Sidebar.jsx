import { useEffect, useState } from "react";
import {
  Link,
  useLocation,
  useNavigate,
} from "react-router-dom";

import {
  crearConversacion,
  listarConversaciones,
} from "../services/api";

function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();

  const [conversaciones, setConversaciones] =
    useState([]);

  const [cargando, setCargando] =
    useState(false);

  async function cargarConversaciones() {
    try {
      const data =
        await listarConversaciones();

      setConversaciones(data);
    } catch (error) {
      console.error(
        "Error cargando conversaciones:",
        error
      );
    }
  }

  useEffect(() => {
    cargarConversaciones();
  }, [location.pathname]);

  async function nuevaConversacion() {
    if (cargando) {
      return;
    }

    try {
      setCargando(true);

      const nueva =
        await crearConversacion(
          "Nueva conversación"
        );

      setConversaciones((anteriores) => [
        nueva,
        ...anteriores,
      ]);

      navigate(
        `/chat?conversation=${nueva.id}`
      );
    } catch (error) {
      console.error(
        "Error creando conversación:",
        error
      );
    } finally {
      setCargando(false);
    }
  }

  return (
    <aside className="sidebar">

      <h1 className="sidebar-logo">
        VAYRONA
      </h1>

      <p
        style={{
          color: "#9ca3af",
          fontSize: "12px",
          marginTop: "-10px",
          marginBottom: "20px",
        }}
      >
        Powered by SYRAE
      </p>

      <nav className="sidebar-nav">
        <Link to="/">
          Dashboard
        </Link>

        <Link to="/chat">
          Chat
        </Link>

        <Link to="/robots">
          Robots
        </Link>

        <Link to="/vision">
          Vision
        </Link>

        <Link to="/projects">
          Projects
        </Link>

        <Link to="/settings">
          Settings
        </Link>
      </nav>

      <div className="conversaciones-panel">
        <button
          className="nueva-conversacion"
          onClick={nuevaConversacion}
          disabled={cargando}
        >
          {cargando
            ? "Creando..."
            : "+ Nueva conversación"}
        </button>

        <h3>Conversaciones</h3>

        <div className="lista-conversaciones">
          {conversaciones.length === 0 ? (
            <p className="sin-conversaciones">
              No hay conversaciones
            </p>
          ) : (
            conversaciones.map(
              (conversacion) => (
                <Link
                  key={conversacion.id}
                  to={`/chat?conversation=${conversacion.id}`}
                  className="conversacion-item"
                >
                  <span>💬</span>

                  <span>
                    {conversacion.titulo ||
                      "Nueva conversación"}
                  </span>
                </Link>
              )
            )
          )}
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
