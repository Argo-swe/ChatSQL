from typing import Optional
from fastapi_camelcase import CamelModel


class PromptDto(CamelModel):
    """Data Transfer Object for handling prompt data.
    
    Attributes:
        prompt (Optional[str]): An optional string representing the prompt.
        debug (Optional[str]): An optional string for debugging information.
    """
    prompt: Optional[str] = None
    debug: Optional[str] = None
