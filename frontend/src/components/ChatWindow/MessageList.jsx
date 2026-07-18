import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";
import { useChat } from "../../context/ChatContext";

export default function MessageList() {
  const { messages } = useChat();
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="scroll-thin flex-1 overflow-y-auto bg-chat-bg py-3">
      {messages.length === 0 ? (
        <p className="mt-10 text-center text-sm text-gray-500">Sem mensagens ainda.</p>
      ) : (
        messages.map((m) => <MessageBubble key={m.id} message={m} />)
      )}
      <div ref={bottomRef} />
    </div>
  );
}
