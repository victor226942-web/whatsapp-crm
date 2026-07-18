import { AuthProvider, useAuth } from "./context/AuthContext";
import { ChatProvider } from "./context/ChatContext";
import Login from "./components/Login";
import Sidebar from "./components/Sidebar/Sidebar";
import ChatWindow from "./components/ChatWindow/ChatWindow";
import QRModal from "./components/QRModal";

function Screen() {
  const { isAuthenticated, checking } = useAuth();

  if (checking) return null; // evita piscar a tela de login enquanto valida o token salvo
  if (!isAuthenticated) return <Login />;

  return (
    <ChatProvider>
      <div className="flex h-screen w-screen bg-panel">
        <Sidebar />
        <ChatWindow />
        <QRModal />
      </div>
    </ChatProvider>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Screen />
    </AuthProvider>
  );
}
