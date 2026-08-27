export default function SearchBar({ value, onChange }) {
  return (
    <div className="relative flex-1 min-w-[220px]">
      <input
        type="text"
        className="w-full py-3 pl-10 pr-10 border border-border-main rounded-xl text-[0.92rem] text-text-main bg-white transition-all duration-200 outline-none placeholder:text-[#9f91ae] focus:border-accent focus:bg-white focus:ring-[4px] focus:ring-accent/30"
        placeholder="Busque pelo nome do projeto ou descrição"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
      {value && (
        <button
          className="absolute right-3 top-1/2 -translate-y-1/2 bg-transparent border-none cursor-pointer text-[0.76rem] text-[#9586a6] px-1 py-0.5 leading-none rounded transition-colors duration-150 hover:text-brand"
          onClick={() => onChange("")}
          aria-label="Limpar busca"
        >
          ✕
        </button>
      )}
    </div>
  );
}
