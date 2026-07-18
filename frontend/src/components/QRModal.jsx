import { useChat } from "../context/ChatContext";

export default function QRModal() {
  const { qrCode, setQrCode, instanceState } = useChat();

  if (!qrCode || instanceState === "open") return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
      <div className="w-80 rounded-lg bg-panel-header p-6 text-center">
        <h3 className="mb-1 text-base font-medium text-gray-100">Conectar o WhatsApp</h3>
        <p className="mb-4 text-xs text-gray-400">
          Abra o WhatsApp no celular → Aparelhos conectados → Conectar um aparelho
        </p>
        <img src={qrCode} alt="QR Code de pareamento" className="mx-auto h-56 w-56 rounded bg-white p-2" />
        <button
          onClick={() => setQrCode(null)}
          className="mt-4 rounded-full bg-white/10 px-4 py-1.5 text-sm text-gray-200 hover:bg-white/20"
        >
          Fechar
        </button>
      </div>
    </div>
  );
}
