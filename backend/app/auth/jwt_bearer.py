from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from auth.jwt_handler import JwtHandler


class JwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(JwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(403, detail="Invalid authentication scheme.")
            if not self._verify_jwt(credentials.credentials):
                raise HTTPException(403, detail="Invalid or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(403, detail="Invalid authorization code.")

    def _verify_jwt(self, token: str) -> bool:
        payload = JwtHandler.decode(token)
        if payload:
            return True
        return False
