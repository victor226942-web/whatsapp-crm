import { HiOutlineQrcode, HiOutlineLogout } from "react-icons/hi";
import { useChat } from "../../context/ChatContext";
import { useAuth } from "../../context/AuthContext";

const STATE_LABEL = { open: "Conectado", connecting: "Conectando…", close: "Desconectado" };
const STATE_DOT = { open: "bg-accent", connecting: "bg-yellow-400", close: "bg-red-500" };

export default function SidebarHeader() {
  const { instanceState, requestQrCode } = useChat();
  const { username, logout } = useAuth();

  return (
    <div className="flex items-center justify-between bg-panel-header px-4 py-3">
      <div className="flex items-center gap-2">
        <span className={`h-2.5 w-2.5 rounded-full ${STATE_DOT[instanceState]}`} />
        <span className="text-sm text-gray-200">{STATE_LABEL[instanceState]}</span>
      </div>
      <div className="flex items-center gap-1">
        {instanceState !== "open" && (
          <button
            onClick={requestQrCode}
            title="Gerar QR Code para conectar"
            className="rounded-full p-2 text-gray-300 hover:bg-white/10"
          >
            <HiOutlineQrcode size={20} />
          </button>
        )}
        <button
          onClick={logout}
          title={`Sair (${username})`}
          className="rounded-full p-2 text-gray-300 hover:bg-white/10"
        >
          <HiOutlineLogout size={18} />
        </button>
      </div>
    </div>
  );
}
