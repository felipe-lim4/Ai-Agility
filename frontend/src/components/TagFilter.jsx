import { useState, useRef, useEffect } from "react";

export default function TagFilter({ tags, selected, onToggle }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    function handleClickOutside(e) {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const label =
    selected.length === 0
      ? "Filtrar por tags"
      : selected.length === 1
        ? selected[0]
        : `${selected.length} tags`;

  return (
    <div className="relative max-sm:w-full" ref={ref}>
      <button
        type="button"
        className="flex items-center justify-between w-[220px] py-3 px-4 border border-border-main rounded-xl text-[0.88rem] text-text-main bg-white transition-all duration-200 outline-none cursor-pointer whitespace-nowrap focus:border-accent focus:ring-[4px] focus:ring-accent/30 max-sm:w-full"
        onClick={() => setOpen((v) => !v)}
      >
        <span className={selected.length === 0 ? "text-[#9f91ae]" : ""}>{label}</span>
        <svg className={`w-3 h-3 text-text-soft transition-transform duration-200 ${open ? "rotate-180" : ""}`} viewBox="0 0 12 12" fill="currentColor"><path d="M2 4l4 4 4-4" /></svg>
      </button>

      {open && (
        <div className="absolute top-full left-0 mt-1.5 w-full min-w-[200px] bg-white border border-border-main rounded-xl shadow-lg z-50 py-1.5 max-h-[260px] overflow-y-auto animate-fade-in">
          {tags.map((tag) => (
            <label
              key={tag}
              className="flex items-center gap-2.5 px-4 py-2 cursor-pointer text-[0.86rem] text-text-main hover:bg-brand-soft/50 transition-colors duration-100"
            >
              <input
                type="checkbox"
                checked={selected.includes(tag)}
                onChange={() => onToggle(tag)}
                className="w-4 h-4 rounded border-border-main text-brand accent-brand cursor-pointer"
              />
              {tag}
            </label>
          ))}
        </div>
      )}
    </div>
  );
}
