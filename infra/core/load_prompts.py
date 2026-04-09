from pathlib import Path
import yaml


def _load_prompts_from_local_yaml() -> list[str]:
    """
    Carrega os prompts de um arquivo YAML local.
    O arquivo deve estar localizado em "infra/core/prompts.yaml" e conter as chaves

    """
    repo_root = Path(__file__).resolve().parent
    local_path = repo_root / "prompts" / "prompts.yaml"
    with local_path.open("r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
    print(f"[load_prompts] Prompts carregados do arquivo local: {local_path}")
    return [
         config_data.get("GENERATE_README", "")
    ]
       
    
def build_prompt() -> list[str]:
    """
    Constrói a lista de prompts a ser utilizada pela aplicação.
    Atualmente, carrega os prompts de um arquivo YAML local.
    """
    return _load_prompts_from_local_yaml()