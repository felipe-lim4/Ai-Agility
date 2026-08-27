# AI Agility

Hub inteligente de documentação de repositórios GitHub que analisa automaticamente projetos e gera READMEs estruturados com enriquecimento via IA (Azure OpenAI).

## Funcionalidades

- **Análise Automática de Repositórios** — Clona e analisa repositórios GitHub extraindo estrutura, dependências e código-fonte
- **Geração de README com IA** — Utiliza Azure OpenAI para gerar documentação completa e estruturada
- **Sistema de Tags Inteligente** — Categorização automática com tags pré-definidas (python, java, fastapi, frontend, ai, devops, etc.)
- **Busca e Filtros** — Pesquisa por nome, descrição e filtragem por tags
- **Acompanhamento de Status** — Monitoramento em tempo real do progresso da geração (SENT → PROCESSING → FINISHED)
- **Download de Markdown** — Exportação dos READMEs gerados em formato `.md`

## Tech Stack

| Camada | Tecnologias |
|--------|-------------|
| **Backend** | Python 3.10+, FastAPI, SQLAlchemy 2 (async), Pydantic 2, Uvicorn |
| **Banco de Dados** | SQLite (aiosqlite) — PostgreSQL suportado |
| **IA** | Azure OpenAI (GPT-4) |
| **Frontend** | React 19, Vite, Tailwind CSS 4, Axios, React-Markdown |

## Arquitetura

O projeto segue o padrão **Clean Architecture** com separação clara de responsabilidades:

```
adapters/          → Controllers REST e DTOs (camada de interface)
application/       → Casos de uso e orquestração de lógica de negócio
domain/            → Entidades, enums e interfaces de repositório
infra/             → Implementações concretas
  ├── azure_services/  → Integração com Azure OpenAI
  ├── core/            → Configuração, logging e prompts
  ├── database/        → Modelos SQLAlchemy e repositórios
  ├── dependencies/    → Injeção de dependências (FastAPI Depends)
  ├── exceptions/      → Tratamento de erros customizado
  └── utils/           → Utilitários de extração de repositório
frontend/          → Aplicação React (SPA)
```

## Pré-requisitos

- Python 3.10+
- Node.js 18+
- Git

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
DB_URL=sqlite+aiosqlite:///./db/persistent.db

AZURE_ENDPOINT=https://<seu-recurso>.openai.azure.com/
OPENAI_API_VERSION=2024-02-15
OPENAI_DEPLOYMENT_NAME=<nome-do-deployment>
API_KEY=<sua-chave>
```

## Execução

### Backend

```bash
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Na inicialização o backend cria as tabelas automaticamente e popula 10 tags padrão.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

O frontend roda em `http://localhost:5173` com proxy automático de `/api/*` para o backend na porta 8000.

## API Endpoints

### READMEs

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/generate_readme` | Inicia geração de README a partir de URL do GitHub |
| `GET` | `/list_documents` | Lista todos os READMEs gerados |
| `GET` | `/get_document/{id}` | Retorna README por ID |
| `PATCH` | `/get_document/{id}` | Atualiza metadados/tags do README |
| `DELETE` | `/delete/{id}` | Remove registro de README |
| `GET` | `/get_documents_by_tag?tag_id=` | Filtra READMEs por tag |

### Tags e Health

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/tags` | Lista todas as tags disponíveis |
| `GET` | `/health` | Health check da aplicação |
| `GET` | `/health/db-sqlite` | Health check do banco de dados |

## Modelo de Dados

```
┌──────────────┐       ┌─────────────┐       ┌──────────┐
│    readme     │──M:N──│  readme_tag  │──M:N──│   tag    │
├──────────────┤       ├─────────────┤       ├──────────┤
│ id (PK)      │       │ readme_id   │       │ id (PK)  │
│ link_origin  │       │ tag_id      │       │ name     │
│ project_name │       └─────────────┘       │ description│
│ summary      │                              └──────────┘
│ description  │
│ tree         │
│ technologies │  (JSON)
│ features     │  (JSON)
│ setup        │  (JSON)
│ usage        │  (JSON)
│ important_notes│ (JSON)
│ links        │  (JSON)
│ status       │  (Enum: SENT|PROCESSING|FINISHED|ERROR)
│ created_at   │
│ updated_at   │
└──────────────┘
```

## Fluxo de Geração

1. Usuário submete URL do repositório GitHub
2. Backend clona o repositório (`git clone --depth 1`)
3. Extrai árvore de arquivos, dependências e código-fonte
4. Envia dados estruturados para Azure OpenAI com prompt em YAML
5. LLM retorna JSON estruturado com documentação completa
6. Sistema persiste o resultado, associa tags e atualiza status para FINISHED
7. Frontend exibe o README gerado com suporte a Markdown