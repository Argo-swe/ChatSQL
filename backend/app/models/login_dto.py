from fastapi_camelcase import CamelModel


class LoginDto(CamelModel):
    username: str
    password: str
