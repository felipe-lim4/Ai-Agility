
import subprocess
import tempfile
from pathlib import Path

def _clone_repository(repo_url: str) -> str:
    temp_dir = tempfile.mkdtemp(prefix="repo_clone_")
    subprocess.run(
        ["git", "clone", "--depth", "1", repo_url, temp_dir],
        check=True,
        capture_output=True,
        text=True,
    )
    return temp_dir


def extract_repository_texts(repo_url: str) -> list[dict[str, str]]:

    repo_path = _clone_repository(repo_url)

    ignored_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv"}
    file_entries = []

    for file_path in Path(repo_path).rglob("*"):
        if not file_path.is_file():
            continue

        relative_parts = set(file_path.relative_to(repo_path).parts)
        if relative_parts & ignored_dirs:
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

    return file_entries