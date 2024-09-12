from fastapi_camelcase import CamelModel


class LoginDto(CamelModel):
    """Data Transfer Object for carrying user login information.

    Attributes:
        username (str): The username provided by the user during login.
        password (str): The password provided by the user during login.
    """
    username: str
    password: str
