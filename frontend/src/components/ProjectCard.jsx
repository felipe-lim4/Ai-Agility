import { techBadgeStyle } from "../data/techColors";

export default function ProjectCard({ project, onClick }) {
  return (
    <article
      className="group bg-white/90 border border-border-main rounded-[20px] p-7 cursor-pointer transition-all duration-200 ease-out flex flex-col gap-5 outline-none shadow-card hover:shadow-card-hover hover:border-accent hover:bg-white focus:shadow-card-hover focus:border-accent focus:bg-white"
      onClick={onClick}
      tabIndex={0}
      onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && onClick()}
      role="button"
      aria-label={`Ver detalhes de ${project.name}`}
    >
      <div className="flex items-center gap-3.5">
        <div className="w-11 h-11 grid place-items-center rounded-xl bg-linear-to-br from-brand to-brand-2 text-white text-[0.9rem] font-bold tracking-wide shrink-0 shadow-sm" aria-hidden="true">
          {project.name.slice(0, 1).toUpperCase()}
        </div>
        <div className="flex-1 min-w-0">
          <h2 className="font-heading text-[1.14rem] font-bold text-text-main m-0 whitespace-nowrap overflow-hidden text-ellipsis">{project.name}</h2>
          <a
            href={project.repoUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-[0.76rem] text-text-soft no-underline whitespace-nowrap overflow-hidden text-ellipsis block mt-0.5 hover:text-brand hover:underline"
            onClick={(e) => e.stopPropagation()}
          >
            {project.repoUrl.replace("https://", "")}
          </a>
        </div>
      </div>

      <p className="text-[0.88rem] text-text-soft leading-relaxed m-0 line-clamp-4">{project.summary}</p>

      <div className="flex flex-col gap-1.5 mt-auto">
        <span className="text-[0.7rem] font-semibold text-text-soft uppercase tracking-[0.06em]">Tags</span>
        <div className="flex flex-wrap gap-1.5">
          {project.tags.map((tag) => (
            <span key={tag} className="text-[0.77rem] text-brand/70 bg-brand-soft px-3 py-1 rounded-full font-medium">#{tag}</span>
          ))}
        </div>
      </div>
      
      <div className="flex flex-col gap-1.5">
        <span className="text-[0.7rem] font-semibold text-text-soft uppercase tracking-[0.06em]">Tecnologias</span>
        <div className="flex flex-wrap gap-1.5">
          {project.technologies.map((tech) => (
            <span key={tech} className="text-[0.76rem] font-semibold px-3 py-[5px] rounded-lg border whitespace-nowrap" style={techBadgeStyle(tech)}>
              {tech}
            </span>
          ))}
        </div>
      </div>

      <div className="pt-4 border-t border-line/60 flex items-center justify-between">
        <span className="text-[0.82rem] font-semibold text-brand/60 transition-all duration-200 group-hover:text-brand group-focus:text-brand">Abrir detalhes</span>
        <span className="text-brand/40 text-sm transition-all duration-200 translate-x-0 group-hover:translate-x-1 group-hover:text-brand group-focus:translate-x-1 group-focus:text-brand" aria-hidden="true">→</span>
      </div>

    </article>
  );
}
