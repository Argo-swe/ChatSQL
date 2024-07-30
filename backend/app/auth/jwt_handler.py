import time
from typing import Dict
import jwt
import os


class JwtHandler:

    JWT_SECRET = os.getenv("JWT_SECRET", "secret_string")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

    @staticmethod
    def __token_response(token: str):
        return {"access_token": token}

    @staticmethod
    def sign(user_id: int) -> Dict[str, str]:
        payload = {"exp": round(time.time()) + 6000, "sub": user_id}  # 100 minuti
        token = jwt.encode(
            payload, JwtHandler.JWT_SECRET, algorithm=JwtHandler.JWT_ALGORITHM
        )
        return JwtHandler.__token_response(token)

    @staticmethod
    def decode(token: str) -> dict | None:
        try:
            decoded_token = jwt.decode(
                token, JwtHandler.JWT_SECRET, algorithms=[JwtHandler.JWT_ALGORITHM]
            )
            # Check if the token is not expired
            if decoded_token.get("exp", 0) >= time.time():
                return decoded_token
            else:
                return None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except jwt.DecodeError:
            return None
