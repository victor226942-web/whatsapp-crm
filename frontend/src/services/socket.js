import { getToken } from "./api";

/**
 * WebSocket nativo, sem socket.io-client — o backend é Django Channels,
 * que fala WS puro. Reconecta sozinho se a conexão cair (o front não pode
 * ficar "mudo" só porque o WebSocket caiu um segundo). O token de sessão
 * vai como query string, porque WebSocket não manda header Authorization.
 */
export function connectSocket(onMessage) {
  const base = import.meta.env.VITE_WS_URL || "ws://localhost:8000/ws/chat/";
  let socket;
  let closedByUser = false;

  function open() {
    const token = getToken();
    const url = `${base}?token=${encodeURIComponent(token || "")}`;
    socket = new WebSocket(url);
    socket.onmessage = (event) => {
      try {
        onMessage(JSON.parse(event.data));
      } catch {
        // ignora frame inválido
      }
    };
    socket.onclose = () => {
      if (!closedByUser) setTimeout(open, 2000); // reconecta em 2s
    };
  }

  open();

  return {
    close() {
      closedByUser = true;
      socket?.close();
    },
  };
}
