import axios from "axios";

const api = axios.create({
  baseURL: "/api",
});

/**
 * Gera um README a partir de um link de repositório.
 * POST /generate_readme
 */
export async function generateReadme(linkOrigin) {
  const { data } = await api.post("/generate_readme", {
    link_origin: linkOrigin,
  });
  return data; // { id: number }
}

/**
 * Lista todos os documentos.
 * GET /list_documents
 */
export async function listDocuments() {
  const { data } = await api.get("/list_documents");
  return data;
}

/**
 * Lista todas as tags disponíveis.
 * GET /tags
 */
export async function listTags() {
  const { data } = await api.get("/tags");
  return data;
}

/**
 * Busca um documento por ID.
 * GET /get_document/:id
 */
export async function getDocumentById(id) {
  const { data } = await api.get(`/get_document/${id}`);
  return data;
}

/**
 * Busca documentos por tag ID.
 * GET /get_documents_by_tag?tag_id=
 */
export async function getDocumentsByTag(tagId) {
  const { data } = await api.get("/get_documents_by_tag", {
    params: { tag_id: tagId },
  });
  return data;
}

/**
 * Atualiza um documento.
 * PATCH /get_document/:id
 */
export async function updateDocument(id, updateData) {
  const { data } = await api.patch(`/get_document/${id}`, updateData);
  return data;
}

/**
 * Deleta um documento.
 * DELETE /delete/:id
 */
export async function deleteDocument(id) {
  const { data } = await api.delete(`/delete/${id}`);
  return data;
}

/**
 * Monta um markdown legível a partir dos campos estruturados do backend.
 */
function buildReadmeMarkdown(doc) {
  const sections = [];

  if (doc.project_name) {
    sections.push(`# ${doc.project_name}`);
  }

  if (doc.description) {
    sections.push(doc.description);
  }

  if (doc.tree) {
    sections.push(`## Estrutura do Projeto\n\n\`\`\`\n${doc.tree}\n\`\`\``);
  }

  const features = doc.features || [];
  if (features.length > 0) {
    sections.push(`## Funcionalidades\n\n${features.map((f) => `- ${f}`).join("\n")}`);
  }

  const techs = doc.technologies || [];
  if (techs.length > 0) {
    sections.push(`## Tecnologias\n\n${techs.map((t) => `- ${t}`).join("\n")}`);
  }

  const setup = doc.setup || {};
  const steps = setup.steps || [];
  if (steps.length > 0) {
    sections.push(`## Como configurar\n\n${steps.map((s, i) => `${i + 1}. ${s}`).join("\n")}`);
  }

  const usage = doc.usage || {};
  const commands = usage.commands || [];
  if (commands.length > 0) {
    sections.push(`## Como usar\n\n\`\`\`bash\n${commands.join("\n")}\n\`\`\``);
  }

  const notes = doc.important_notes || [];
  if (notes.length > 0) {
    sections.push(`## Notas Importantes\n\n${notes.map((n) => `> ${n}`).join("\n\n")}`);
  }

  const links = doc.links || [];
  if (links.length > 0) {
    sections.push(`## Links\n\n${links.map((l) => `- ${l}`).join("\n")}`);
  }

  return sections.join("\n\n");
}

/**
 * Converte a resposta do backend para o formato esperado pelo frontend.
 */
export function mapBackendToProject(doc) {
  return {
    id: doc.id,
    name: doc.project_name || "sem-nome",
    repoUrl: doc.link_origin,
    summary: doc.summary || "",
    tags: (doc.tags || []).map((t) => t.name),
    technologies: doc.technologies || [],
    status: doc.status,
    description: doc.description || "",
    tree: doc.tree || "",
    features: doc.features || [],
    setup: doc.setup || {},
    usage: doc.usage || {},
    important_notes: doc.important_notes || [],
    links: doc.links || [],
    readme: buildReadmeMarkdown(doc),
    created_at: doc.created_at,
    updated_at: doc.updated_at,
  };
}
