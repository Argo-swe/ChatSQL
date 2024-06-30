from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.jwt_handler import JwtHandler

class JwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(JwtBearer, self).__call__(request)
        if(credentials):
            if not credentials.scheme == "Bearer":
                raise HTTPException(403, detail= "Invalid authentication scheme.")
            if not self._verifyJwt(credentials.credentials):
                raise HTTPException(403, detail= "Invalid or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(403, detail= "Invalid authorization code.")

    def _verifyJwt(self, token: str) -> bool:
        try:
            payload = JwtHandler.decode(token)
        except:
            payload = None
        if(payload):
            return True
        return False
