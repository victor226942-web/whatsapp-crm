import { createContext, useContext, useEffect, useState } from "react";
import { api, clearToken, getToken, setToken } from "../services/api";

const AuthContext = createContext(null);
export const useAuth = () => useContext(AuthContext);

export function AuthProvider({ children }) {
  const [username, setUsername] = useState(null);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      setChecking(false);
      return;
    }
    api.get("/auth/me/")
      .then(({ data }) => setUsername(data.username))
      .catch(() => clearToken())
      .finally(() => setChecking(false));
  }, []);

  const login = async (user, pass) => {
    const { data } = await api.post("/auth/login/", { username: user, password: pass });
    setToken(data.token);
    setUsername(data.username);
  };

  const logout = async () => {
    try { await api.post("/auth/logout/"); } catch { /* token já pode ter expirado */ }
    clearToken();
    setUsername(null);
  };

  return (
    <AuthContext.Provider value={{ username, isAuthenticated: !!username, checking, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
