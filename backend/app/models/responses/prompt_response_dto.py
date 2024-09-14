from models.prompt_dto import PromptDto
from models.responses.response_dto import ResponseDto


class PromptResponseDto(ResponseDto):
    """Data Transfer Object for prompt responses.

    Attributes:
        data (PromptDto | None): Object representing prompt-related data (if present).
    """

    data: PromptDto | None
