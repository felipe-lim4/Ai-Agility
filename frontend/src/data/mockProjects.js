export const mockProjects = [
  {
    id: 1,
    name: "auth-service",
    repoUrl: "https://github.com/org/auth-service",
    summary:
      "Serviço centralizado de autenticação e autorização responsável por gerenciar login via JWT e OAuth2, controle de acesso baseado em papéis (RBAC), integração com provedores externos como Google e GitHub, além de auditoria completa de acessos e sessões ativas na plataforma. O serviço conta com cache distribuído via Redis para otimizar a validação de tokens, suporte a refresh tokens com rotação automática, expiração configurável de sessões e logs estruturados para conformidade com políticas de segurança da organização.",
    tags: ["backend", "segurança", "api"],
    technologies: ["Node.js", "Express", "JWT", "PostgreSQL"],
    readme: `# auth-service

Serviço centralizado de autenticação e autorização para a organização.

## Funcionalidades

- Autenticação via JWT e OAuth2
- Controle de acesso baseado em papéis (RBAC)
- Integração com provedores externos (Google, GitHub)
- Auditoria de acessos

## Tecnologias

- **Runtime:** Node.js 20
- **Framework:** Express
- **Banco de dados:** PostgreSQL
- **Cache:** Redis

## Como usar

\`\`\`bash
npm install
cp .env.example .env
npm run dev
\`\`\`

## Variáveis de Ambiente

| Variável | Descrição |
|----------|-----------|
| \`DATABASE_URL\` | URL de conexão com o PostgreSQL |
| \`JWT_SECRET\` | Segredo para assinar tokens JWT |
| \`REDIS_URL\` | URL de conexão com o Redis |

## Endpoints

- \`POST /auth/login\` — Autenticação de usuário
- \`POST /auth/refresh\` — Renovação de token
- \`POST /auth/logout\` — Encerramento de sessão
- \`GET /auth/me\` — Dados do usuário autenticado
`,
  },
  {
    id: 2,
    name: "dashboard-ui",
    repoUrl: "https://github.com/org/dashboard-ui",
    summary:
      "Interface web de monitoramento em tempo real que exibe métricas da plataforma com gráficos interativos via Chart.js, filtros dinâmicos por período e categoria, suporte a temas claro e escuro, e exportação de relatórios em PDF e CSV para análise offline. Possui sistema de widgets arrastáveis para personalização do layout, notificações em tempo real via WebSocket quando métricas ultrapassam thresholds configurados, e páginas de drill-down para análise detalhada de cada indicador.",
    tags: ["frontend", "ui", "monitoramento"],
    technologies: ["React", "TypeScript", "Chart.js", "Tailwind CSS"],
    readme: `# dashboard-ui

Dashboard de monitoramento em tempo real para acompanhamento de métricas da plataforma.

## Funcionalidades

- Gráficos interativos com Chart.js
- Filtros dinâmicos por período e categoria
- Suporte a temas claro e escuro
- Exportação de relatórios em PDF/CSV

## Tecnologias

- **Framework:** React 18
- **Linguagem:** TypeScript
- **Estilização:** Tailwind CSS
- **Gráficos:** Chart.js / React-Chartjs-2

## Como executar

\`\`\`bash
npm install
npm run dev
\`\`\`

## Build

\`\`\`bash
npm run build
\`\`\`

## Estrutura do Projeto

\`\`\`
src/
  components/   # Componentes reutilizáveis
  pages/        # Páginas da aplicação
  hooks/        # Custom hooks
  utils/        # Funções utilitárias
\`\`\`
`,
  },
  {
    id: 3,
    name: "notification-worker",
    repoUrl: "https://github.com/org/notification-worker",
    summary:
      "Worker assíncrono multicanal para envio de notificações por e-mail (SendGrid/SMTP), SMS (Twilio) e push (Firebase FCM), com suporte a filas via RabbitMQ, retry automático em caso de falhas, priorização de mensagens e monitoramento de entregas em tempo real. Inclui sistema de templates dinâmicos para personalização de conteúdo por canal, rate limiting configurável para evitar throttling de provedores, dead-letter queue para mensagens que excederam o número máximo de tentativas, e dashboard de métricas de envio integrado ao Grafana.",
    tags: ["backend", "workers", "mensageria"],
    technologies: ["Python", "Celery", "RabbitMQ", "Redis"],
    readme: `# notification-worker

Worker assíncrono responsável pelo envio de notificações multicanal.

## Canais Suportados

- E-mail (via SendGrid / SMTP)
- SMS (via Twilio)
- Push Notifications (via Firebase FCM)

## Tecnologias

- **Linguagem:** Python 3.11
- **Task Queue:** Celery
- **Broker:** RabbitMQ
- **Cache:** Redis

## Configuração

\`\`\`bash
pip install -r requirements.txt
cp .env.example .env
celery -A worker worker --loglevel=info
\`\`\`

## Variáveis de Ambiente

| Variável | Descrição |
|----------|-----------|
| \`RABBITMQ_URL\` | URL de conexão com o RabbitMQ |
| \`SENDGRID_API_KEY\` | Chave da API SendGrid |
| \`TWILIO_SID\` | SID da conta Twilio |
`,
  },
  {
    id: 4,
    name: "file-storage-api",
    repoUrl: "https://github.com/org/file-storage-api",
    summary:
      "API RESTful em Go para upload (multipart e stream), download direto e via URLs pré-assinadas, e gerenciamento completo de arquivos com armazenamento na AWS S3, distribuição via CloudFront CDN e metadados persistidos em PostgreSQL para rastreabilidade. Suporta múltiplos buckets por ambiente, validação de tipos MIME, geração automática de thumbnails para imagens, versionamento de arquivos com histórico de alterações, e controle de acesso granular por projeto e usuário com políticas definidas via IAM.",
    tags: ["backend", "api", "storage"],
    technologies: ["Go", "AWS S3", "CloudFront", "PostgreSQL"],
    readme: `# file-storage-api

API RESTful para gerenciamento de arquivos com armazenamento na AWS S3.

## Funcionalidades

- Upload de arquivos (multipart e stream)
- Download direto e via URL pré-assinada
- Integração com CloudFront CDN
- Suporte a múltiplos buckets e ambientes

## Tecnologias

- **Linguagem:** Go 1.22
- **Storage:** AWS S3
- **CDN:** CloudFront
- **Banco de dados:** PostgreSQL (metadados)

## Como executar

\`\`\`bash
go mod tidy
go run main.go
\`\`\`

## Endpoints

- \`POST /files\` — Upload de arquivo
- \`GET /files/:id\` — Download de arquivo
- \`DELETE /files/:id\` — Remoção de arquivo
- \`GET /files\` — Listagem de arquivos
`,
  },
  {
    id: 5,
    name: "mobile-app",
    repoUrl: "https://github.com/org/mobile-app",
    summary:
      "Aplicativo móvel multiplataforma para iOS e Android desenvolvido com React Native e Expo, com funcionalidades offline via SQLite, sincronização automática em background, notificações push nativas, autenticação biométrica e suporte a temas claro e escuro. O app utiliza Redux Toolkit para gerenciamento de estado global, React Navigation v6 para navegação entre telas, deep linking para integração com outros serviços da organização, e pipeline de CI/CD via EAS Build para distribuição automatizada nas lojas.",
    tags: ["mobile", "frontend", "offline"],
    technologies: ["React Native", "Expo", "SQLite", "Redux"],
    readme: `# mobile-app

Aplicativo móvel multiplataforma desenvolvido com React Native e Expo.

## Funcionalidades

- Suporte offline com sincronização automática
- Notificações push nativas
- Autenticação biométrica
- Temas claro e escuro

## Tecnologias

- **Framework:** React Native + Expo
- **Estado:** Redux Toolkit
- **Banco local:** SQLite (via Expo SQLite)
- **Navegação:** React Navigation v6

## Como executar

\`\`\`bash
npm install
npx expo start
\`\`\`

## Build

\`\`\`bash
eas build --platform all
\`\`\`
`,
  },
  {
    id: 6,
    name: "data-pipeline",
    repoUrl: "https://github.com/org/data-pipeline",
    summary:
      "Pipeline ETL para ingestão, transformação e carregamento de grandes volumes de dados, orquestrado pelo Apache Airflow com processamento distribuído via Spark e armazenamento no Google BigQuery, incluindo DAGs configuráveis para vendas, eventos de usuário e tabelas de analytics. Conta com monitoramento de execução via Airflow UI, alertas automáticos por Slack em caso de falhas, particionamento inteligente de tabelas para otimização de custos, data quality checks integrados em cada etapa do pipeline, e documentação automática de linhagem de dados.",
    tags: ["data", "etl", "backend"],
    technologies: ["Python", "Apache Airflow", "Spark", "BigQuery"],
    readme: `# data-pipeline

Pipeline ETL para processamento de grandes volumes de dados.

## Arquitetura

\`\`\`
Fonte → Ingestão → Transformação → Carga → BI/Analytics
\`\`\`

## Tecnologias

- **Orquestração:** Apache Airflow
- **Processamento:** Apache Spark
- **Data Warehouse:** Google BigQuery
- **Linguagem:** Python 3.11

## Como executar localmente

\`\`\`bash
docker-compose up -d
pip install -r requirements.txt
airflow db init
airflow webserver
\`\`\`

## DAGs Disponíveis

- \`ingest_sales_daily\` — Ingestão diária de vendas
- \`transform_user_events\` — Transformação de eventos de usuário
- \`load_analytics_tables\` — Carga nas tabelas de analytics
`,
  },
];

export const allTags = [
  ...new Set(mockProjects.flatMap((p) => p.tags)),
];

export const mockRepoData = [
  {
    name: "new-microservice",
    summary:
      "Microsserviço responsável pelo gerenciamento de entidades de negócio com API REST e documentação OpenAPI.",
    tags: ["backend", "api", "microsserviços"],
    technologies: ["Node.js", "Fastify", "MongoDB", "Docker"],
    readme: `# new-microservice

Microsserviço gerado automaticamente a partir do repositório informado.

## Funcionalidades

- CRUD completo de entidades
- Documentação automática via OpenAPI/Swagger
- Containerização com Docker
- Health check endpoint

## Tecnologias

- **Runtime:** Node.js 20
- **Framework:** Fastify
- **Banco de dados:** MongoDB
- **Container:** Docker

## Como executar

\`\`\`bash
npm install
npm run dev
\`\`\`

## Endpoints

- \`GET /health\` — Health check
- \`GET /items\` — Listar itens
- \`POST /items\` — Criar item
- \`PUT /items/:id\` — Atualizar item
- \`DELETE /items/:id\` — Remover item
`,
  },
  {
    name: "frontend-portal",
    summary:
      "Portal web responsivo com autenticação, painel de controle e integração com APIs internas da organização.",
    tags: ["frontend", "ui", "portal"],
    technologies: ["Vue.js", "Vite", "Pinia", "Tailwind CSS"],
    readme: `# frontend-portal

Portal web responsivo para acesso aos serviços da organização.

## Funcionalidades

- Autenticação SSO
- Painel de controle personalizável
- Integração com APIs internas
- Responsivo para mobile e desktop

## Tecnologias

- **Framework:** Vue.js 3
- **Build:** Vite
- **Estado:** Pinia
- **Estilo:** Tailwind CSS

## Como executar

\`\`\`bash
npm install
npm run dev
\`\`\`
`,
  },
  {
    name: "analytics-service",
    summary:
      "Serviço de analytics para coleta, processamento e visualização de métricas de uso da plataforma em tempo real.",
    tags: ["data", "backend", "monitoramento"],
    technologies: ["Python", "FastAPI", "ClickHouse", "Grafana"],
    readme: `# analytics-service

Serviço de analytics para monitoramento em tempo real da plataforma.

## Funcionalidades

- Coleta de eventos em tempo real
- Dashboards no Grafana
- Retenção configurável de dados
- Alertas baseados em thresholds

## Tecnologias

- **Linguagem:** Python 3.11
- **Framework:** FastAPI
- **Banco:** ClickHouse
- **Visualização:** Grafana

## Como executar

\`\`\`bash
pip install -r requirements.txt
uvicorn main:app --reload
\`\`\`
`,
  },
];
