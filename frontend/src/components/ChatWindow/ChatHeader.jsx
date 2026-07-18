import { RiRobot2Fill, RiPauseCircleLine } from "react-icons/ri";
import { useChat } from "../../context/ChatContext";

export default function ChatHeader() {
  const { activeContact, toggleAiPaused } = useChat();

  return (
    <div className="flex items-center justify-between border-b border-white/10 bg-panel-header px-4 py-2.5">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-panel text-sm font-medium text-gray-300">
          {(activeContact.push_name || activeContact.phone).slice(0, 2).toUpperCase()}
        </div>
        <div>
          <h2 className="text-sm font-medium text-gray-100">
            {activeContact.push_name || activeContact.phone}
          </h2>
          <p className="text-xs text-gray-400">{activeContact.phone}</p>
        </div>
      </div>

      <button
        onClick={() => toggleAiPaused(activeContact)}
        className={`flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-medium ${
          activeContact.is_ai_paused
            ? "bg-yellow-400/10 text-yellow-400"
            : "bg-accent/10 text-accent"
        }`}
        title="Alternar entre resposta automática da IA e atendimento manual"
      >
        {activeContact.is_ai_paused ? (
          <>
            <RiPauseCircleLine size={15} /> Atendimento manual — retomar IA
          </>
        ) : (
          <>
            <RiRobot2Fill size={15} /> IA respondendo — assumir conversa
          </>
        )}
      </button>
    </div>
  );
}
