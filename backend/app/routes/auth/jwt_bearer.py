from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from routes.auth.jwt_handler import JwtHandler
from tools.exceptions import LoginError


class JwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        """Initialize the JwtBearer security scheme."""
        super(JwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """Extract and verify the JWT from the request.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            str: The credentials (JWT token) if valid.

        Raises:
            HTTPException: If the authentication scheme is not 'Bearer', or if the token is invalid or expired.
        """
        credentials = await super(JwtBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    403, detail=LoginError.invalid_authentication_scheme()
                )
            if not self._verify_jwt(credentials.credentials):
                raise HTTPException(403, detail=LoginError.invalid_expired_token())
            return credentials.credentials
        else:
            raise HTTPException(403, detail=LoginError.invalid_authorization_code())

    def _verify_jwt(self, token: str) -> bool:
        """Verify the JWT token.

        Args:
            token (str): The JWT token to verify.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        payload = JwtHandler.decode(token)
        if payload:
            return True
        return False
