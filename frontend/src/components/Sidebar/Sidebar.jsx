import SidebarHeader from "./SidebarHeader";
import SearchBar from "./SearchBar";
import ChatList from "./ChatList";

export default function Sidebar() {
  return (
    <div className="flex w-full max-w-[380px] flex-shrink-0 flex-col border-r border-white/10 bg-panel">
      <SidebarHeader />
      <SearchBar />
      <ChatList />
    </div>
  );
}
