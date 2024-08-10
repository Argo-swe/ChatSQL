from typing import Optional
from fastapi_camelcase import CamelModel


class PromptDto(CamelModel):
    prompt: str
    debug: Optional[str] = None
