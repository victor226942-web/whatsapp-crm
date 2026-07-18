import { useState } from "react";
import { IoSend } from "react-icons/io5";
import { useChat } from "../../context/ChatContext";

export default function MessageInput() {
  const [text, setText] = useState("");
  const { sendMessage, activeContact } = useChat();

  const handleSend = () => {
    if (!text.trim()) return;
    sendMessage(text);
    setText("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const aiIsActive = !activeContact.is_ai_paused;

  return (
    <div className="border-t border-white/10 bg-panel-header px-4 py-3">
      {aiIsActive && (
        <p className="mb-2 text-[11px] text-gray-500">
          A IA está respondendo automaticamente. Envie uma mensagem aqui pra assumir a conversa.
        </p>
      )}
      <div className="flex items-end gap-2">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Digite uma mensagem"
          rows={1}
          className="scroll-thin flex-1 resize-none rounded-lg bg-panel px-3 py-2 text-sm text-gray-100 placeholder-gray-500 outline-none"
        />
        <button
          onClick={handleSend}
          disabled={!text.trim()}
          className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-full bg-accent text-white disabled:opacity-40"
        >
          <IoSend size={16} />
        </button>
      </div>
    </div>
  );
}
