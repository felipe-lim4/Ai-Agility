export default function Header() {
  return (
    <header className="bg-linear-to-br from-[rgba(43,18,76,0.92)] to-[rgba(82,43,91,0.9)] border-b border-[rgba(216,169,241,0.28)] backdrop-blur-[10px] sticky top-0 z-100">
      <div className="w-[92%] max-w-[1800px] mx-auto px-6 min-h-[74px] flex items-center max-[480px]:w-full max-[480px]:px-4">
        <div className="flex items-center gap-3.5">
          <span className="w-[38px] h-[38px] rounded-[10px] grid place-items-center border border-[rgba(216,169,241,0.48)] bg-[rgba(216,169,241,0.14)] text-[#f7ebff] text-[0.84rem] font-extrabold tracking-[0.07em]" aria-hidden="true">
            AI Agility
          </span>
          <div className="flex flex-col gap-0.5">
            <h1 className="font-heading text-[1.18rem] font-extrabold text-white m-0 tracking-[-0.02em]">AI Agility</h1>
            <span className="text-[0.8rem] text-[rgba(241,220,253,0.86)] max-[480px]:text-[0.75rem]">Hub de documentações dos seus projetos GitHub</span>
          </div>
        </div>
      </div>
    </header>
  );
}
