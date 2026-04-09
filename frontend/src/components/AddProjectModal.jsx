import { useState } from "react";
import { mockRepoData } from "../data/mockProjects";

function randomMockData() {
  return mockRepoData[Math.floor(Math.random() * mockRepoData.length)];
}

function extractNameFromUrl(url) {
  try {
    const parts = url.replace(/\/$/, "").split("/");
    return parts[parts.length - 1] || "novo-projeto";
  } catch {
    return "novo-projeto";
  }
}

export default function AddProjectModal({ onClose, onAdd }) {
  const [repoUrl, setRepoUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!repoUrl.trim()) {
      setError("Informe o link do repositório.");
      return;
    }
    if (!repoUrl.startsWith("http")) {
      setError("Informe uma URL válida (ex: https://github.com/org/repo).");
      return;
    }
    setError("");
    setLoading(true);

    // Simulate async AI enrichment
    setTimeout(() => {
      const mock = randomMockData();
      const name = extractNameFromUrl(repoUrl);
      onAdd({
        id: Date.now(),
        name,
        repoUrl: repoUrl.trim(),
        summary: mock.summary,
        tags: mock.tags,
        technologies: mock.technologies,
        readme: mock.readme.replace(/new-microservice|frontend-portal|analytics-service/g, name),
      });
      setLoading(false);
      onClose();
    }, 1800);
  };

  return (
    <div
      className="fixed inset-0 bg-black/30 backdrop-blur-[3px] z-[1000] flex items-center justify-center p-6 animate-fade-in"
      onClick={(e) => !loading && e.target === e.currentTarget && onClose()}
      role="dialog"
      aria-modal="true"
    >
      <div className="bg-white rounded-[20px] w-full max-w-[480px] shadow-lg border border-[#e0d0ec] animate-slide-up overflow-hidden">
        <div className="flex items-center justify-between px-5 py-4 bg-[#fcf9ff] border-b border-line">
          <h2 className="font-heading text-[1.05rem] font-bold text-text-main m-0">Cadastrar Projeto</h2>
          <button
            className="bg-white border border-[#ddcfee] text-[#7f6d97] w-8 h-8 rounded-[10px] cursor-pointer text-[0.8rem] flex items-center justify-center transition-all duration-150 hover:border-accent hover:text-brand disabled:opacity-50 disabled:cursor-not-allowed"
            onClick={onClose}
            disabled={loading}
            aria-label="Fechar"
          >
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-5 flex flex-col gap-[18px]">
          <div className="flex flex-col gap-2">
            <label className="text-[0.8rem] font-semibold text-text-soft uppercase tracking-[0.05em]" htmlFor="repoUrl">
              Link do Repositório
            </label>
            <input
              id="repoUrl"
              type="text"
              className="px-3.5 py-[11px] border border-border-main rounded-xl text-[0.9rem] text-text-main outline-none transition-all duration-200 focus:border-accent focus:ring-[4px] focus:ring-accent/30 disabled:bg-[#f5f5f5] disabled:text-[#999]"
              placeholder="https://github.com/org/repo"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              disabled={loading}
              autoFocus
            />
            {error && <span className="text-[0.8rem] text-[#be2e34]">{error}</span>}
          </div>

          {loading && (
            <div className="flex items-center gap-4 bg-[#f7f0fc] border border-[#e4d5f1] rounded-xl p-4">
              <div className="w-7 h-7 border-3 border-[rgba(82,43,91,0.22)] border-t-brand rounded-full animate-spin shrink-0" />
              <div>
                <p className="text-[0.86rem] font-semibold text-brand-2 m-0 mb-[3px]">Gerando documentação...</p>
                <p className="text-[0.78rem] text-[#7b6a91] m-0">
                  Analisando repositório e enriquecendo informações com IA
                </p>
              </div>
            </div>
          )}

          {!loading && (
            <div className="flex items-start gap-2.5 bg-[#f8f1fd] border border-[#e4d6f2] rounded-[10px] p-3.5">
              <span className="w-5 h-5 rounded-full border border-[#d8b8eb] text-brand grid place-items-center text-[0.74rem] font-bold shrink-0" aria-hidden="true">i</span>
              <p className="text-[0.82rem] text-[#745f8b] m-0 leading-[1.5]">
                O sistema irá gerar automaticamente o resumo, tags e tecnologias
                do projeto com base no repositório informado.
              </p>
            </div>
          )}

          <div className="flex gap-2.5 justify-end">
            <button
              type="button"
              className="px-[18px] py-2.5 border border-[#ddcfee] rounded-xl bg-white text-[#715f89] text-[0.86rem] font-semibold cursor-pointer transition-all duration-350 hover:bg-[#faf6fd] hover:border-accent disabled:opacity-50 disabled:cursor-not-allowed"
              onClick={onClose}
              disabled={loading}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="px-[22px] py-2.5 border border-[rgba(43,18,76,0.35)] rounded-xl bg-linear-to-br from-brand to-brand-2 text-white text-[0.86rem] font-semibold cursor-pointer transition-all duration-150 hover:brightness-[1.03] disabled:opacity-60 disabled:cursor-not-allowed disabled:translate-y-0"
              disabled={loading}
            >
              {loading ? "Processando..." : "Cadastrar"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
