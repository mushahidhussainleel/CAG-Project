import jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv , find_dotenv

load_dotenv(find_dotenv())

# -------------------------------
# Config / Secret
# -------------------------------
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 90 # 1 hour and 30 mint

# -------------------------------
# Create JWT Access Token
# -------------------------------
def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    """
    Creates a JWT token with expiration.
    Args:
        data: Dictionary to encode inside the token (e.g., user_id, email)
        expires_delta: Minutes until token expires
    Returns:
        JWT token string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

# -------------------------------
# Verify JWT Access Token
# -------------------------------
def verify_access_token(token: str) -> Optional[dict]:
    """
    Decodes and verifies the JWT token.
    Returns payload if valid, else None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Token is invalid
        return None
