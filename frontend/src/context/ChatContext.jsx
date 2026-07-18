import { createContext, useCallback, useContext, useEffect, useRef, useState } from "react";
import { api, INSTANCE_NAME } from "../services/api";
import { connectSocket } from "../services/socket";

const ChatContext = createContext(null);
export const useChat = () => useContext(ChatContext);

export function ChatProvider({ children }) {
  const [instanceState, setInstanceState] = useState("close"); // open | connecting | close
  const [qrCode, setQrCode] = useState(null);
  const [contacts, setContacts] = useState([]);
  const [activeContact, setActiveContact] = useState(null);
  const [messages, setMessages] = useState([]);
  const [search, setSearch] = useState("");
  const socketRef = useRef(null);
  const activeContactRef = useRef(null);
  activeContactRef.current = activeContact;

  const fetchContacts = useCallback(async () => {
    const { data } = await api.get("/contacts/");
    setContacts(data);
  }, []);

  const fetchStatus = useCallback(async () => {
    try {
      const { data } = await api.get("/evolution/status/", { params: { instance: INSTANCE_NAME } });
      setInstanceState(data.state);
    } catch {
      setInstanceState("close");
    }
  }, []);

  const requestQrCode = useCallback(async () => {
    const { data } = await api.get("/evolution/qrcode/", { params: { instance: INSTANCE_NAME } });
    if (data.qrcode) setQrCode(data.qrcode);
  }, []);

  const openContact = useCallback(async (contact) => {
    setActiveContact(contact);
    const { data } = await api.get(`/contacts/${contact.id}/messages/`);
    setMessages(data);
  }, []);

  const sendMessage = useCallback(async (text) => {
    if (!activeContact || !text.trim()) return;
    // otimista: mostra na hora, o backend confirma via WebSocket também
    const optimistic = {
      id: `tmp-${Date.now()}`,
      role: "agent",
      content: text,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, optimistic]);
    await api.post("/send-message/", { contact_id: activeContact.id, text });
  }, [activeContact]);

  const toggleAiPaused = useCallback(async (contact) => {
    const { data } = await api.patch(`/contacts/${contact.id}/`, {
      is_ai_paused: !contact.is_ai_paused,
    });
    setContacts((prev) => prev.map((c) => (c.id === data.id ? data : c)));
    setActiveContact((prev) => (prev?.id === data.id ? data : prev));
  }, []);

  useEffect(() => {
    fetchContacts();
    fetchStatus();

    socketRef.current = connectSocket((frame) => {
      if (frame.type === "status_change") {
        setInstanceState(frame.payload.state);
        if (frame.payload.state === "open") setQrCode(null);
      }

      if (frame.type === "new_message") {
        const { contact_id, message } = frame.payload;

        // se o chat aberto agora é esse contato, injeta a mensagem
        if (activeContactRef.current?.id === contact_id) {
          setMessages((prev) => [...prev.filter((m) => !String(m.id).startsWith("tmp-")), message]);
        }

        // sobe o contato pro topo da lista e atualiza a prévia (como o WhatsApp faz)
        setContacts((prev) => {
          const idx = prev.findIndex((c) => c.id === contact_id);
          if (idx === -1) {
            fetchContacts(); // contato novo que ainda não estava na lista
            return prev;
          }
          const updated = { ...prev[idx], last_message: message.content, last_message_at: message.created_at };
          const rest = prev.filter((c) => c.id !== contact_id);
          return [updated, ...rest];
        });
      }
    });

    return () => socketRef.current?.close();
  }, [fetchContacts, fetchStatus]);

  const filteredContacts = contacts.filter((c) => {
    const term = search.trim().toLowerCase();
    if (!term) return true;
    return (c.push_name || c.phone).toLowerCase().includes(term);
  });

  return (
    <ChatContext.Provider
      value={{
        instanceState, qrCode, setQrCode, requestQrCode,
        contacts: filteredContacts, search, setSearch,
        activeContact, openContact, messages, sendMessage, toggleAiPaused,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}
