from models.responses.response_dto import ResponseDto


class AuthResponseDto(ResponseDto):
    data: dict | None
