export const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
const TOKEN_KEY = "clearclause_token";

export const getToken = () => localStorage.getItem(TOKEN_KEY);
export const setToken = (t) => localStorage.setItem(TOKEN_KEY, t);
export const clearToken = () => localStorage.removeItem(TOKEN_KEY);

// App.jsx registers a function here that logs the user out if the token expires
let onUnauthorized = () => {};
export function setUnauthorizedHandler(fn) {
  onUnauthorized = fn;
}

export async function apiFetch(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  let res;
  try {
    res = await fetch(`${API}${path}`, { ...options, headers });
  } catch {
    throw new Error("Can't reach the backend. Is uvicorn running?");
  }

  let data = null;
  try {
    data = await res.json();
  } catch {
    // response had no JSON body
  }

  // A saved token that no longer works (expired or user deleted)
  if (res.status === 401 && token) onUnauthorized();

  if (!res.ok) {
    const detail = data?.detail;
    const message = Array.isArray(detail)
      ? detail[0]?.msg || "Please check your details."
      : detail;
    throw new Error(message || "Something went wrong.");
  }
  return data;
}