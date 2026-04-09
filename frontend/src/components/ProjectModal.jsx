import { useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { techBadgeStyle } from "../data/techColors";

export default function ProjectModal({ project, onClose }) {
  useEffect(() => {
    document.body.style.overflow = "hidden";
    const handleKey = (e) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", handleKey);
    return () => {
      document.body.style.overflow = "";
      window.removeEventListener("keydown", handleKey);
    };
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 bg-black/30 backdrop-blur-[3px] z-[1000] flex items-center justify-center p-6 animate-fade-in max-sm:p-3"
      onClick={(e) => e.target === e.currentTarget && onClose()}
      role="dialog"
      aria-modal="true"
      aria-label={`Detalhes do projeto ${project.name}`}
    >
      <div className="bg-white rounded-[20px] w-full max-w-[980px] max-h-[90vh] flex flex-col shadow-lg animate-slide-up overflow-hidden border border-[#e0d0ec]">
        <div className="flex items-center justify-between px-5 py-4 border-b border-line bg-[#fcf9ff] shrink-0">
          <div className="flex items-center gap-3.5">
            <span className="w-[34px] h-[34px] grid place-items-center rounded-[10px] bg-brand-soft text-brand text-[0.8rem] font-bold tracking-[0.04em]" aria-hidden="true">
              {project.name.slice(0, 1).toUpperCase()}
            </span>
            <div>
              <h2 className="font-heading text-[1.14rem] font-bold text-text-main m-0 mb-1">{project.name}</h2>
              <a
                href={project.repoUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="text-[0.76rem] text-[#7a6791] no-underline hover:text-brand hover:underline"
              >
                {project.repoUrl}
              </a>
            </div>
          </div>
          <button
            className="bg-white border border-[#ddcfee] text-[#7f6d97] w-[34px] h-[34px] rounded-[10px] cursor-pointer text-[0.85rem] flex items-center justify-center transition-all duration-150 shrink-0 hover:border-accent hover:text-brand"
            onClick={onClose}
            aria-label="Fechar modal"
          >
            ✕
          </button>
        </div>

        <div className="grid grid-cols-[300px_1fr] overflow-hidden flex-1 min-h-0 max-sm:grid-cols-1 max-sm:grid-rows-[auto_1fr]">
          <div className="p-5 border-r border-line overflow-y-auto flex flex-col gap-[18px] bg-[#faf7fd] max-sm:border-r-0 max-sm:border-b max-sm:border-line max-sm:overflow-y-visible">
            <div className="flex flex-col gap-2">
              <h3 className="text-[0.72rem] font-bold text-[#8a78a1] uppercase tracking-[0.06em] m-0">Resumo</h3>
              <p className="text-[0.84rem] text-text-soft leading-[1.65] m-0">{project.summary}</p>
            </div>

            <div className="flex flex-col gap-2">
              <h3 className="text-[0.72rem] font-bold text-[#8a78a1] uppercase tracking-[0.06em] m-0">Tecnologias</h3>
              <div className="flex flex-wrap gap-1.5">
                {project.technologies.map((tech) => (
                  <span
                    key={tech}
                    className="text-[0.72rem] font-semibold px-2.5 py-1 rounded-full border"
                    style={techBadgeStyle(tech)}
                  >
                    {tech}
                  </span>
                ))}
              </div>
            </div>

            <div className="flex flex-col gap-2">
              <h3 className="text-[0.72rem] font-bold text-[#8a78a1] uppercase tracking-[0.06em] m-0">Tags</h3>
              <div className="flex flex-wrap gap-1.5">
                {project.tags.map((tag) => (
                  <span key={tag} className="text-[0.76rem] text-brand bg-[#f2e6fb] px-2.5 py-1 rounded-full">
                    #{tag}
                  </span>
                ))}
              </div>
            </div>
          </div>

          <div className="flex flex-col overflow-hidden">
            <h3 className="text-[0.75rem] font-bold text-[#7f6b98] uppercase tracking-[0.08em] m-0 px-5 py-3.5 border-b border-line bg-white shrink-0">README</h3>
            <div className="readme-prose p-5 overflow-y-auto flex-1 text-[0.88rem] leading-[1.7] text-[#3b2a53]">
              <ReactMarkdown>{project.readme}</ReactMarkdown>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
