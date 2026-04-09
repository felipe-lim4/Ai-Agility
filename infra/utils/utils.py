import subprocess
import tempfile
from pathlib import Path

IGNORED_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
IGNORED_FILES = {
    "readme.md", "readme.txt", "readme",
    "requirements.txt", "pipfile", "pyproject.toml",
    "package.json", "pom.xml", "build.gradle",
    "pipfile.lock", "package-lock.json", "yarn.lock",
}


def _clone_repository(repo_url: str) -> str:
    temp_dir = tempfile.mkdtemp(prefix="repo_clone_")
    subprocess.run(
        ["git", "clone", "--depth", "1", repo_url, temp_dir],
        check=True,
        capture_output=True,
        text=True,
    )
    return temp_dir


def _build_tree_paths(repo_path: str) -> str:
    """Constrói a árvore de arquivos usando git ls-tree."""
    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _extract_dependencies(repo_path: str) -> list[str]:
    """Extrai dependências lendo arquivos comuns de configuração."""
    import json
    root = Path(repo_path)
    deps: list[str] = []

    for filename in ["requirements.txt", "Pipfile", "pyproject.toml", "package.json", "pom.xml", "build.gradle"]:
        dep_file = root / filename
        if not dep_file.exists():
            continue
        try:
            content = dep_file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        if filename == "package.json":
            try:
                data = json.loads(content)
                for section in ("dependencies", "devDependencies"):
                    if isinstance(data.get(section), dict):
                        deps.extend(data[section].keys())
            except json.JSONDecodeError:
                pass
        else:
            for line in content.splitlines():
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("[") and not line.startswith("<"):
                    deps.append(line)

    return list(dict.fromkeys(deps))

def _extract_readme_original(repo_path: str) -> str | None:
    """Tenta extrair o conteúdo do README original, se existir."""
    root = Path(repo_path)
    for filename in ["README.md", "README.txt", "README"]:
        readme_file = root / filename
        if readme_file.exists() and readme_file.is_file():
            try:
                return readme_file.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
    return None

def extract_repository_code(repo_url: str) -> dict:
    repo_path = _clone_repository(repo_url)

    tree = _build_tree_paths(repo_path)
    dependencies = _extract_dependencies(repo_path)
    readme_original = _extract_readme_original(repo_path)
    file_entries = []
    for file_path in Path(repo_path).rglob("*"):
        if not file_path.is_file():
            continue

        relative_parts = set(file_path.relative_to(repo_path).parts)
        if relative_parts & IGNORED_DIRS:
            continue

        if file_path.name.lower() in IGNORED_FILES:
            continue

        try:
            content = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        except OSError:
            continue

        file_entries.append(
            {
                "path": str(file_path.relative_to(repo_path)).replace("\\", "/"),
                "content": content,
            }
        )

    return {
        "tree": tree,
        "dependencies": dependencies,
        "readme_original": readme_original,
        "files": file_entries,
    }