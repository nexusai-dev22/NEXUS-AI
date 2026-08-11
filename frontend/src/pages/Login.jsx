import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/api";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState("");

  const iniciarSesion = async (e) => {
    e.preventDefault();

    if (!email.trim() || !password) {
      setError("Completa el correo y la contraseña.");
      return;
    }

    setCargando(true);
    setError("");

    try {
      const datos = await login(email, password);

      console.log("Login correcto:", datos);

      const token = localStorage.getItem("token");

      if (!token) {
        throw new Error("No se recibió el token.");
      }

      navigate("/chat");
    } catch (error) {
      console.error("Error de login:", error);
      setError(error.message || "No se pudo iniciar sesión.");
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>VAYRONA</h1>

        <p
          style={{
            color: "#6b7280",
            marginTop: "-10px",
            marginBottom: "20px",
            fontWeight: "500",
          }}
        >
          Powered by SYRAE
        </p>

        <p>Inicia sesión para continuar</p>

        <form onSubmit={iniciarSesion}>
          <input
            type="email"
            placeholder="Correo electrónico"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={cargando}
          />

          <input
            type="password"
            placeholder="Contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={cargando}
          />

          {error && (
            <div className="login-error">
              {error}
            </div>
          )}

          <button type="submit" disabled={cargando}>
            {cargando
              ? "Iniciando sesión..."
              : "Iniciar sesión"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
