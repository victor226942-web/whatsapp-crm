import { useState } from "react";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(username, password);
    } catch {
      setError("Usuário ou senha inválidos");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen w-screen items-center justify-center bg-chat-bg">
      <form onSubmit={handleSubmit} className="w-72 rounded-lg bg-panel-header p-6">
        <h1 className="mb-1 text-lg font-medium text-gray-100">WhatsApp CRM</h1>
        <p className="mb-5 text-xs text-gray-400">Entre com sua conta de atendente</p>

        <label className="mb-1 block text-xs text-gray-400">Usuário</label>
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="mb-3 w-full rounded bg-panel px-3 py-2 text-sm text-gray-100 outline-none"
          autoFocus
        />

        <label className="mb-1 block text-xs text-gray-400">Senha</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="mb-4 w-full rounded bg-panel px-3 py-2 text-sm text-gray-100 outline-none"
        />

        {error && <p className="mb-3 text-xs text-red-400">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-full bg-accent py-2 text-sm font-medium text-white disabled:opacity-50"
        >
          {loading ? "Entrando…" : "Entrar"}
        </button>
      </form>
    </div>
  );
}
