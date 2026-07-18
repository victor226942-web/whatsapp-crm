import { IoSearchOutline } from "react-icons/io5";
import { useChat } from "../../context/ChatContext";

export default function SearchBar() {
  const { search, setSearch } = useChat();

  return (
    <div className="bg-panel px-3 py-2">
      <div className="flex items-center gap-3 rounded-lg bg-panel-header px-3 py-1.5">
        <IoSearchOutline className="text-gray-400" size={16} />
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Pesquisar conversa"
          className="w-full bg-transparent text-sm text-gray-200 placeholder-gray-500 outline-none"
        />
      </div>
    </div>
  );
}
