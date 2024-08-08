from models.prompt_dto import PromptDto
from models.responses.response_dto import ResponseDto


class PromptResponseDto(ResponseDto):
    data: PromptDto | None
