import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get secret and algorithm from environment or fallback
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

if not JWT_SECRET:
    raise EnvironmentError(
        "JWT_SECRET is not set in the environment."
        "Please check your .env file.")


def create_token(username: str) -> str:
    """
    Create a JWT token for a given username.

    Parameters:
    - username (str): The authenticated username to encode

    Returns:
    - str: Encoded JWT token
    """
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=1),  # Token expiration time
        "iat": datetime.utcnow(),  # Issued at time
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_token(token: str) -> str or None:
    """
    Decode a JWT token and return the subject (username) if valid.

    Parameters:
    - token (str): JWT token to decode

    Returns:
    - str: Username if valid
    - None: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        # print("Token expired")
        return None
    except jwt.InvalidTokenError:
        # print("Invalid token")
        return None
