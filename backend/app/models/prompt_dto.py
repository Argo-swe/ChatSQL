from typing import Optional
from fastapi_camelcase import CamelModel


class PromptDto(CamelModel):
    prompt: Optional[str] = None
    debug: Optional[str] = None
