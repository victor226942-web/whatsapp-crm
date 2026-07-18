import { format, isToday } from "date-fns";
import { ptBR } from "date-fns/locale";
import { RiRobot2Fill, RiPauseCircleLine } from "react-icons/ri";
import { useChat } from "../../context/ChatContext";

function formatTime(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  return isToday(d) ? format(d, "HH:mm") : format(d, "dd/MM", { locale: ptBR });
}

export default function ChatList() {
  const { contacts, activeContact, openContact } = useChat();

  if (contacts.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center px-8 text-center text-sm text-gray-500">
        Nenhuma conversa ainda. Assim que uma mensagem chegar no WhatsApp, ela aparece aqui.
      </div>
    );
  }

  return (
    <div className="scroll-thin flex-1 overflow-y-auto">
      {contacts.map((contact) => {
        const isActive = activeContact?.id === contact.id;
        return (
          <button
            key={contact.id}
            onClick={() => openContact(contact)}
            className={`flex w-full items-center gap-3 border-b border-white/5 px-3 py-3 text-left hover:bg-white/5 ${
              isActive ? "bg-white/10" : ""
            }`}
          >
            <div className="flex h-11 w-11 flex-shrink-0 items-center justify-center rounded-full bg-panel-header text-sm font-medium text-gray-300">
              {(contact.push_name || contact.phone).slice(0, 2).toUpperCase()}
            </div>
            <div className="min-w-0 flex-1">
              <div className="flex items-baseline justify-between">
                <span className="truncate text-sm font-medium text-gray-100">
                  {contact.push_name || contact.phone}
                </span>
                <span className="ml-2 flex-shrink-0 text-[11px] text-gray-500">
                  {formatTime(contact.last_message_at)}
                </span>
              </div>
              <div className="flex items-center gap-1">
                {contact.is_ai_paused ? (
                  <RiPauseCircleLine className="flex-shrink-0 text-yellow-400" size={13} title="IA pausada" />
                ) : (
                  <RiRobot2Fill className="flex-shrink-0 text-accent" size={13} title="IA respondendo" />
                )}
                <p className="truncate text-xs text-gray-400">{contact.last_message || "Sem mensagens"}</p>
              </div>
            </div>
          </button>
        );
      })}
    </div>
  );
}
