import ChatHeader from "./ChatHeader";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";
import { useChat } from "../../context/ChatContext";

export default function ChatWindow() {
  const { activeContact } = useChat();

  if (!activeContact) {
    return (
      <div className="flex flex-1 flex-col items-center justify-center bg-chat-bg text-gray-500">
        <p className="text-sm">Selecione uma conversa para começar a atender</p>
      </div>
    );
  }

  return (
    <div className="flex flex-1 flex-col">
      <ChatHeader />
      <MessageList />
      <MessageInput />
    </div>
  );
}
