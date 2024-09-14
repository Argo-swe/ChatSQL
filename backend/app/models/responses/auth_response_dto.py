from models.responses.response_dto import ResponseDto


class AuthResponseDto(ResponseDto):
    """Data Transfer Object for authentication responses.

    Attributes:
        data (dict | None): Contains authentication-related data (if present).
    """

    data: dict | None
