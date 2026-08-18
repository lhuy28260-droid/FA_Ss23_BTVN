from enum import Enum
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status


SECRET_KEY = "secret-key-demo"
ALGORITHM = "HS256"


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


def create_access_token(user_id: str, role: Role):
    payload = {
        "sub": user_id,
        "role": role.value,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")
        role = payload.get("role")

        if not user_id or not role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        return {
            "user_id": user_id,
            "role": role
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )