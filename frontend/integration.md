# Documentação de Integração — AI Agility (Frontend React ↔ Backend FastAPI)

> **Objetivo**: conectar o frontend React existente a uma API FastAPI (Python) que se comunica com um banco de dados PostgreSQL e com o serviço de IA da Azure (Azure OpenAI).

---

## 1. Modelo de dados atual no frontend

Cada projeto exibido no frontend segue este formato (extraído de `src/data/mockProjects.js`):

```jsonc
{
  "id": 1,                        // number — identificador único
  "name": "Nome do Projeto",      // string — nome exibido no card
  "repoUrl": "https://github.com/...", // string — URL do repositório
  "summary": "Texto longo...",    // string — resumo gerado pela IA
  "techs": ["React", "Node.js"], // string[] — tecnologias detectadas
  "tags": ["IA", "Backend"],     // string[] — tags/categorias
  "readme": "# Conteúdo MD..."   // string — markdown do README
}
```

---

## 2. Schemas Pydantic (Backend)

```python
# app/schemas/project.py
from pydantic import BaseModel, HttpUrl

class ProjectCreate(BaseModel):
    """Payload enviado pelo frontend ao adicionar um projeto."""
    repo_url: HttpUrl

class ProjectOut(BaseModel):
    """Resposta retornada para o frontend."""
    id: int
    name: str
    repo_url: str
    summary: str
    techs: list[str]
    tags: list[str]
    readme: str

    class Config:
        from_attributes = True

class ProjectListOut(BaseModel):
    projects: list[ProjectOut]
    tags: list[str]           # lista unificada de todas as tags
```

---

## 3. Endpoints da API

| Método | Rota | Descrição | Request Body | Response |
|--------|------|-----------|-------------|----------|
| `GET` | `/api/projects` | Lista todos os projetos | — | `ProjectListOut` |
| `GET` | `/api/projects/{id}` | Detalhe de um projeto | — | `ProjectOut` |
| `POST` | `/api/projects` | Cria projeto (aciona IA) | `ProjectCreate` | `ProjectOut` |
| `DELETE` | `/api/projects/{id}` | Remove um projeto | — | `204 No Content` |
| `GET` | `/api/tags` | Lista todas as tags únicas | — | `string[]` |

---

## 4. Fluxo de criação de projeto (sequência)

```
Frontend                        Backend (FastAPI)              Azure OpenAI           GitHub API        PostgreSQL
   │                                │                              │                     │                 │
   │  POST /api/projects            │                              │                     │                 │
   │  { repo_url }                  │                              │                     │                 │
   │ ─────────────────────────────► │                              │                     │                 │
   │                                │  GET repo metadata           │                     │                 │
   │                                │ ──────────────────────────────────────────────────► │                 │
   │                                │  ◄─── { name, readme, lang } ──────────────────── │                 │
   │                                │                              │                     │                 │
   │                                │  POST /openai/deployments/   │                     │                 │
   │                                │  { readme, languages }       │                     │                 │
   │                                │ ───────────────────────────► │                     │                 │
   │                                │  ◄── { summary, techs, tags} │                     │                 │
   │                                │                              │                     │                 │
   │                                │  INSERT project              │                     │                 │
   │                                │ ─────────────────────────────────────────────────────────────────── ►│
   │                                │  ◄─── project row ──────────────────────────────────────────────── │
   │                                │                              │                     │                 │
   │  ◄── 201 ProjectOut ───────── │                              │                     │                 │
   │                                │                              │                     │                 │
```

---

## 5. Exemplo de prompt para Azure OpenAI

```python
# app/services/ai_service.py
import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

SYSTEM_PROMPT = """Você é um assistente técnico. Dado o README de um repositório GitHub
e a lista de linguagens detectadas, retorne EXATAMENTE um JSON com:
{
  "summary": "resumo de 2-4 parágrafos em português do Brasil",
  "techs": ["tecnologia1", "tecnologia2"],
  "tags": ["tag1", "tag2"]
}
Responda SOMENTE com o JSON, sem markdown."""


async def enrich_project(readme: str, languages: list[str]) -> dict:
    """Chama Azure OpenAI e retorna summary, techs e tags."""
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"README:\n{readme}\n\nLinguagens: {', '.join(languages)}"},
        ],
        temperature=0.3,
        max_tokens=1024,
    )
    import json
    return json.loads(response.choices[0].message.content)
```

---

## 6. Alternativa assíncrona (processamento lento)

Se o ciclo GitHub → Azure AI demorar mais de ~5 s, considere um fluxo em duas etapas:

```
POST /api/projects  →  201  { id, status: "processing" }
GET  /api/projects/{id}  →  200  { ..., status: "ready" }
```

O frontend pode fazer polling a cada 3 s ou usar WebSocket:

```javascript
// polling simples
const poll = async (id) => {
  const res = await fetch(`${API}/api/projects/${id}`);
  const data = await res.json();
  if (data.status === 'ready') return data;
  await new Promise(r => setTimeout(r, 3000));
  return poll(id);
};
```

---

## 7. Mudanças necessárias no frontend

### 7.1 Variável de ambiente

Criar `.env` na raiz do projeto:

```env
VITE_API_URL=http://localhost:8000
```

### 7.2 Serviço de API (`src/services/api.js` — novo arquivo)

```javascript
const API = import.meta.env.VITE_API_URL;

export async function fetchProjects() {
  const res = await fetch(`${API}/api/projects`);
  if (!res.ok) throw new Error('Erro ao buscar projetos');
  return res.json(); // { projects: [...], tags: [...] }
}

export async function createProject(repoUrl) {
  const res = await fetch(`${API}/api/projects`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ repo_url: repoUrl }),
  });
  if (!res.ok) throw new Error('Erro ao criar projeto');
  return res.json(); // ProjectOut
}

export async function deleteProject(id) {
  const res = await fetch(`${API}/api/projects/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Erro ao deletar projeto');
}
```

### 7.3 Alterações em `App.jsx`

```diff
+ import { fetchProjects, createProject } from './services/api';

  // Substituir useState inicial:
- const [projects, setProjects] = useState(mockProjects);
+ const [projects, setProjects] = useState([]);
+ const [allTags, setAllTags] = useState([]);
+
+ useEffect(() => {
+   fetchProjects().then(data => {
+     setProjects(data.projects);
+     setAllTags(data.tags);
+   });
+ }, []);

  // Substituir handleAddProject:
- const handleAddProject = (newProject) => {
-   setProjects(prev => [newProject, ...prev]);
- };
+ const handleAddProject = async (repoUrl) => {
+   const newProject = await createProject(repoUrl);
+   setProjects(prev => [newProject, ...prev]);
+ };
```

### 7.4 Alterações em `AddProjectModal.jsx`

Remover a simulação com `setTimeout` e `mockRepoData`, substituindo por:

```javascript
const handleSubmit = async () => {
  if (!repoUrl.trim()) return;
  setLoading(true);
  try {
    await onAdd(repoUrl);   // App.jsx cuida da chamada à API
    onClose();
  } catch {
    alert('Erro ao processar repositório.');
  } finally {
    setLoading(false);
  }
};
```

---

## 8. Mapeamento de campos (frontend ↔ backend)

| Frontend (JS) | Backend (Python) | Banco (SQL) | Observação |
|---------------|-----------------|-------------|------------|
| `id` | `id` | `id SERIAL PK` | Auto-increment |
| `name` | `name` | `name VARCHAR(255)` | Do GitHub |
| `repoUrl` | `repo_url` | `repo_url TEXT UNIQUE` | camelCase ↔ snake_case |
| `summary` | `summary` | `summary TEXT` | Gerado pela IA |
| `techs` | `techs` | `techs TEXT[]` | Array PostgreSQL |
| `tags` | `tags` | `tags TEXT[]` | Array PostgreSQL |
| `readme` | `readme` | `readme TEXT` | Markdown cru |

---

## 9. Schema SQL (PostgreSQL)

```sql
CREATE TABLE IF NOT EXISTS projects (
    id       SERIAL PRIMARY KEY,
    name     VARCHAR(255)   NOT NULL,
    repo_url TEXT           NOT NULL UNIQUE,
    summary  TEXT           NOT NULL DEFAULT '',
    techs    TEXT[]         NOT NULL DEFAULT '{}',
    tags     TEXT[]         NOT NULL DEFAULT '{}',
    readme   TEXT           NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_projects_tags ON projects USING GIN (tags);
```

---

## 10. CORS (FastAPI)

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Agility API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev
        "https://seu-dominio.com", # produção
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 11. Variáveis de ambiente do backend (`.env`)

```env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/ai_agility
AZURE_OPENAI_API_KEY=sua-chave
AZURE_OPENAI_ENDPOINT=https://seu-recurso.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
```

---

## 12. Estrutura sugerida do backend

```
backend/
├── app/
│   ├── main.py              # FastAPI app + CORS + routers
│   ├── config.py            # Settings via pydantic-settings
│   ├── database.py          # Engine + SessionLocal (asyncpg)
│   ├── models/
│   │   └── project.py       # SQLAlchemy model
│   ├── schemas/
│   │   └── project.py       # Pydantic schemas
│   ├── routers/
│   │   └── projects.py      # Endpoints CRUD
│   └── services/
│       ├── ai_service.py    # Azure OpenAI
│       └── github_service.py# GitHub API (fetch README + langs)
├── requirements.txt
├── .env
└── alembic/                 # migrations
```

---

## Resumo rápido de integração

1. **Backend**: implementar os 5 endpoints listados na seção 3
2. **IA**: usar o prompt da seção 5 para gerar `summary`, `techs` e `tags`
3. **Frontend**: criar `src/services/api.js` (seção 7.2), ajustar `App.jsx` (seção 7.3) e `AddProjectModal.jsx` (seção 7.4)
4. **CORS**: configurar origens permitidas (seção 10)
5. **Env vars**: configurar `.env` em ambos os lados (seções 7.1 e 11)