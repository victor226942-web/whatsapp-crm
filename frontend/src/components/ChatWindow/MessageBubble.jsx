import { format } from "date-fns";

const OUTGOING_ROLES = ["assistant", "agent"];

export default function MessageBubble({ message }) {
  const isOutgoing = OUTGOING_ROLES.includes(message.role);
  const isAi = message.role === "assistant";

  return (
    <div className={`flex ${isOutgoing ? "justify-end" : "justify-start"} px-4 py-0.5`}>
      <div
        className={`max-w-[65%] rounded-lg px-3 py-2 text-sm shadow ${
          isOutgoing ? "bg-bubble-out text-gray-50" : "bg-bubble-in text-gray-100"
        }`}
      >
        {isAi && <span className="mb-0.5 block text-[10px] font-medium text-accent">IA</span>}
        <p className="whitespace-pre-wrap break-words">{message.content}</p>
        <span className="float-right ml-2 mt-1 text-[10px] text-gray-400">
          {format(new Date(message.created_at), "HH:mm")}
        </span>
      </div>
    </div>
  );
}
