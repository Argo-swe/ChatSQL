import time
from typing import Dict
import jwt


class JwtHandler:

    #TODO: Gestione dei segreti
    JWT_SECRET = "secret_string"
    JWT_ALGORITHM = "HS256"


    @staticmethod
    def __tokenResponse(token : str):
        return {
            "access_token": token
        }

    @staticmethod
    def sign() -> Dict[str, str]:
        payload = {
        "expires": time.time() + 6000 # 100 minuti
        }
        token = jwt.encode( payload, JwtHandler.JWT_SECRET, algorithm =JwtHandler.JWT_ALGORITHM)
        return JwtHandler.__tokenResponse(token)
    
    @staticmethod
    def decode(token: str) -> dict|None:
        try:
            decoded_token = jwt.decode(token, JwtHandler.JWT_SECRET, algorithms=[JwtHandler.JWT_ALGORITHM])
            return decoded_token if decoded_token["expires"] >= time.time() else None
        except:
            return None