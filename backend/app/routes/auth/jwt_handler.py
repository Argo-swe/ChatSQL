import time
from typing import Any, Dict, Optional
import jwt
import os


class JwtHandler:

    JWT_SECRET = os.getenv("JWT_SECRET", "secret_string")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

    @staticmethod
    def __token_response(token: str):
        """Create a response structure for the JWT token."""
        return {"access_token": token}

    @staticmethod
    def sign(user_id: int) -> Dict[str, str]:
        """Generate a JWT token for a given user ID.

        Args:
            user_id (int): The ID of the user for whom the token is generated.

        Returns:
            Dict[str, str]: A dictionary containing the JWT token.
        """
        payload = {"exp": round(time.time()) + 6000, "sub": user_id}  # 100 minutes
        token = jwt.encode(
            payload, JwtHandler.JWT_SECRET, algorithm=JwtHandler.JWT_ALGORITHM
        )
        return JwtHandler.__token_response(token)

    @staticmethod
    def decode(token: str) -> Optional[Dict[str, Any]]:
        """Decode and verify a JWT token.

        Args:
            token (str): The JWT token to decode and verify.

        Returns:
            Optional[Dict[str, Any]]: The decoded token payload if the token is valid and not expired, otherwise None.
        """
        try:
            decoded_token = jwt.decode(
                token, JwtHandler.JWT_SECRET, algorithms=[JwtHandler.JWT_ALGORITHM]
            )
            # Check if the token is not expired
            if decoded_token.get("exp", 0) >= time.time():
                return decoded_token
            else:
                return None
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.DecodeError):
            return None
