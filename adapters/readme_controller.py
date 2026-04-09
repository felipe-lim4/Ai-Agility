from fastapi import APIRouter, Depends, HTTPException

from adapters.dtos.readme import (
    DeleteReadmeResponse,
    GenerateReadmeRequest,
    GenerateReadmeResponse,
    ReadmeResponse,
    TagResponse,
    UpdateReadmeRequest,
)
from application.readme.readme_usecase import (
    DeleteReadmeUseCase,
    GenerateReadmeUseCase,
    GetReadmeByIdUseCase,
    GetReadmesByTagUseCase,
    ListDocumentsUseCase,
    UpdateReadmeUseCase,
)
from domain.entities.readme_entity import ReadmeData
from domain.entities.tag_entity import TagData
from infra.dependencies.readme_dependencies import (
    get_delete_readme_use_case,
    get_generate_readme_use_case,
    get_list_documents_use_case,
    get_readme_by_id_use_case,
    get_readmes_by_tag_use_case,
    get_update_readme_use_case,
)


def _tag_to_response(tag: TagData) -> TagResponse:
    return TagResponse(id=tag.id, name=tag.name, description=tag.description)


def _readme_to_response(readme: ReadmeData) -> ReadmeResponse:
    return ReadmeResponse(
        id=readme.id,
        link_origin=readme.link_origin,
        project_name=readme.project_name,
        summary=readme.summary,
        description=readme.description,
        tree=readme.tree,
        technologies=readme.technologies,
        features=readme.features,
        setup=readme.setup,
        usage=readme.usage,
        important_notes=readme.important_notes,
        links=readme.links,
        status=readme.status,
        created_at=readme.created_at,
        updated_at=readme.updated_at,
        tags=[_tag_to_response(tag) for tag in readme.tags],
    )


router = APIRouter(tags=["readme"])


@router.post("/generate_readme", response_model=GenerateReadmeResponse)
async def generate_readme(
    payload: GenerateReadmeRequest,
    use_case: GenerateReadmeUseCase = Depends(get_generate_readme_use_case),
) -> GenerateReadmeResponse:
    readme_id = await use_case.execute(payload.link_origin)
    return GenerateReadmeResponse(id=readme_id)


@router.get("/list_documents", response_model=list[ReadmeResponse])
async def list_documents(
    use_case: ListDocumentsUseCase = Depends(get_list_documents_use_case),
) -> list[ReadmeResponse]:
    readmes = await use_case.execute()
    return [_readme_to_response(readme) for readme in readmes]


@router.get("/get_document/{id}", response_model=ReadmeResponse)
async def get_document(
    id: int,
    use_case: GetReadmeByIdUseCase = Depends(get_readme_by_id_use_case),
) -> ReadmeResponse:
    readme = await use_case.execute(id)
    if readme is None:
        raise HTTPException(status_code=404, detail="Readme not found")
    return _readme_to_response(readme)


@router.get("/get_documents_by_tag", response_model=list[ReadmeResponse])
async def get_documents_by_tag(
    tag_id: int,
    use_case: GetReadmesByTagUseCase = Depends(get_readmes_by_tag_use_case),
) -> list[ReadmeResponse]:
    readmes = await use_case.execute(tag_id)
    return [_readme_to_response(readme) for readme in readmes]


@router.patch("/get_document/{id}", response_model=ReadmeResponse)
async def update_document(
    id: int,
    payload: UpdateReadmeRequest,
    use_case: UpdateReadmeUseCase = Depends(get_update_readme_use_case),
) -> ReadmeResponse:
    update_data = payload.model_dump(exclude_unset=True)
    readme = await use_case.execute(id, update_data)
    if readme is None:
        raise HTTPException(status_code=404, detail="Readme not found")
    return _readme_to_response(readme)


@router.delete("/delete/{id}", response_model=DeleteReadmeResponse)
async def delete_document(
    id: int,
    use_case: DeleteReadmeUseCase = Depends(get_delete_readme_use_case),
) -> DeleteReadmeResponse:
    success = await use_case.execute(id)
    if not success:
        raise HTTPException(status_code=404, detail="Readme not found")
    return DeleteReadmeResponse(success=True)