import { useState, useMemo } from "react";
import Header from "./components/Header";
import SearchBar from "./components/SearchBar";
import TagFilter from "./components/TagFilter";
import ProjectCard from "./components/ProjectCard";
import ProjectModal from "./components/ProjectModal";
import AddProjectModal from "./components/AddProjectModal";
import { mockProjects } from "./data/mockProjects";

export default function App() {
  const [projects, setProjects] = useState(mockProjects);
  const [search, setSearch] = useState("");
  const [selectedTags, setSelectedTags] = useState([]);
  const [activeProject, setActiveProject] = useState(null);
  const [showAddModal, setShowAddModal] = useState(false);

  const tags = useMemo(
    () => [...new Set(projects.flatMap((p) => p.tags))],
    [projects]
  );

  const filtered = useMemo(() => {
    const q = search.toLowerCase();
    return projects.filter((p) => {
      const matchesSearch =
        !q ||
        p.name.toLowerCase().includes(q) ||
        p.tags.some((t) => t.toLowerCase().includes(q)) ||
        p.summary.toLowerCase().includes(q);
      const matchesTag = selectedTags.length === 0 || selectedTags.some((t) => p.tags.includes(t));
      return matchesSearch && matchesTag;
    });
  }, [projects, search, selectedTags]);

  function handleTagToggle(tag) {
    setSelectedTags((prev) =>
      prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]
    );
  }

  function handleAddProject(project) {
    setProjects((prev) => [project, ...prev]);
  }

  return (
    <div className="min-h-screen text-text-main">
      <Header />

      <main className="w-[92%] max-w-[1800px] mx-auto px-6 pt-[38px] pb-14 max-sm:w-full max-sm:px-4 max-sm:pt-6 max-sm:pb-10">
        <div className="bg-white/72 border border-border-main backdrop-blur-[12px] rounded-[18px] p-[18px] flex gap-3 items-stretch mb-[18px] shadow-sm max-sm:p-3.5 max-sm:flex-col">
            <SearchBar value={search} onChange={setSearch} />
            {tags.length > 0 && (
              <TagFilter
                tags={tags}
                selected={selectedTags}
                onToggle={handleTagToggle}
              />
            )}
            <button
              className="flex items-center gap-1.5 justify-center px-5 py-[11px] bg-brand text-white border border-[rgba(43,18,76,0.35)] rounded-xl text-[0.88rem] font-semibold cursor-pointer whitespace-nowrap shadow-btn transition-all duration-[480ms] ease-out hover:brightness-[1.3] hover:shadow-btn-hover active:translate-y-0 max-sm:w-full max-sm:px-3.5 max-sm:text-[0.85rem]"
              onClick={() => setShowAddModal(true)}
            >
              <svg className="w-4 h-4" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" /></svg>
              Novo Projeto
            </button>
        </div>

        <div className="flex items-center justify-between mb-[18px] px-1 max-sm:gap-2.5 max-sm:items-start max-sm:flex-col">
          <span className="text-[0.8rem] text-text-soft font-semibold tracking-[0.03em] uppercase">
            {filtered.length}{" "}
            {filtered.length === 1 ? "projeto encontrado" : "projetos encontrados"}
          </span>
          {(search || selectedTags.length > 0) && (
            <button
              className="bg-white/65 border border-border-main text-[0.8rem] text-text-main cursor-pointer font-semibold px-3 py-2 rounded-[10px] transition-all duration-150 ease-out hover:bg-white hover:border-accent"
              onClick={() => {
                setSearch("");
                setSelectedTags([]);
              }}
            >
              Limpar filtros
            </button>
          )}
        </div>

        {filtered.length > 0 ? (
          <div className="grid grid-cols-2 gap-5 max-sm:grid-cols-1">
            {filtered.map((project) => (
              <ProjectCard
                key={project.id}
                project={project}
                onClick={() => setActiveProject(project)}
              />
            ))}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-[70px] px-6 text-center rounded-[18px] border border-dashed border-[#dbcbe9] bg-white/56">
            <span className="w-12 h-12 rounded-full grid place-items-center border border-[#dbcbe9] text-[1.6rem] mb-4 text-brand" aria-hidden="true">○</span>
            <p className="text-[1.06rem] font-semibold text-text-main m-0 mb-2">Nenhum projeto encontrado</p>
            <p className="text-[0.86rem] text-text-soft m-0">
              Tente ajustar os filtros ou cadastrar um novo projeto.
            </p>
          </div>
        )}
      </main>

      {activeProject && (
        <ProjectModal
          project={activeProject}
          onClose={() => setActiveProject(null)}
        />
      )}

      {showAddModal && (
        <AddProjectModal
          onClose={() => setShowAddModal(false)}
          onAdd={handleAddProject}
        />
      )}
    </div>
  );
}
