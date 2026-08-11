const API_URL = "http://127.0.0.1:8000";

export async function login(email, password) {
  const body = new URLSearchParams();

  body.append("username", email);
  body.append("password", password);

  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Error al iniciar sesión");
  }

  localStorage.setItem("token", data.access_token);

  if (data.usuario) {
    localStorage.setItem("usuario", JSON.stringify(data.usuario));
  }

  return data;
}

export function obtenerToken() {
  return localStorage.getItem("token");
}

export function cerrarSesion() {
  localStorage.removeItem("token");
  localStorage.removeItem("usuario");
}

export async function crearConversacion(
  titulo = "Nueva conversación",
) {
  const token = obtenerToken();

  if (!token) {
    throw new Error("No hay sesión iniciada.");
  }

  const response = await fetch(`${API_URL}/conversations`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ titulo }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Error al crear conversación");
  }

  return data;
}

export async function listarConversaciones() {
  const token = obtenerToken();

  if (!token) {
    throw new Error("No hay sesión iniciada.");
  }

  const response = await fetch(`${API_URL}/conversations`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Error al obtener conversaciones");
  }

  return data;
}

export async function enviarMensaje(
  conversationId,
  rol,
  contenido,
) {
  const token = obtenerToken();

  if (!token) {
    throw new Error("No hay sesión iniciada.");
  }

  const response = await fetch(
    `${API_URL}/conversations/${conversationId}/messages`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        rol,
        contenido,
      }),
    },
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Error al enviar mensaje");
  }

  return data;
}

export async function listarMensajes(conversationId) {
  const token = obtenerToken();

  if (!token) {
    throw new Error("No hay sesión iniciada.");
  }

  const response = await fetch(
    `${API_URL}/conversations/${conversationId}/messages`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Error al obtener mensajes");
  }

  return data;
}
