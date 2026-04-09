from infra.core.config import settings
from pydantic import BaseModel
from openai import AzureOpenAI

logger = settings.logger

class StructuredInput(BaseModel):
    repo_url: str
    tree: str
    dependencies: list[str]
    readme_original: str | None = None
    files: list[dict]


class LLMService:

    def __init__(self):
        self.api_version = settings.OPENAI_API_VERSION
        self.azure_endpoint = settings.AZURE_ENDPOINT
        self.api_key = settings.API_KEY
        self.deployment = settings.OPENAI_DEPLOYMENT_NAME

    def _get_azure_client(self):
        return AzureOpenAI(
            api_version=self.api_version,
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key,
        )


    def get_response_from_azure_openai(self, prompt: str, structured_input: StructuredInput) -> str:
        logger.info("[LLMService] Sending request to Azure OpenAI (deployment=%s, files=%d)",
                    self.deployment, len(structured_input.files))
        client = self._get_azure_client()
        input_json = structured_input.model_dump_json()
        response = client.chat.completions.create(
            model=self.deployment,
            messages=[{
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": input_json,
            }],
            max_tokens=4096,
            temperature=1.0,
            top_p=1.0,
        )
        logger.info("[LLMService] Received response from Azure OpenAI")
        return response.choices[0].message.content