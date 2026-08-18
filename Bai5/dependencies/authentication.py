from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from database import get_db
from models.models import User
from security import decode_access_token


# ==========================================
# HTTP BEARER
# ==========================================

security_scheme = HTTPBearer()


# ==========================================
# CURRENT USER
# ==========================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security_scheme
    ),
    db: Session = Depends(get_db)
) -> User:

    # 1. Lấy JWT từ Authorization Header
    token = credentials.credentials

    # 2. Decode và kiểm tra JWT
    try:
        payload = decode_access_token(token)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # 3. Lấy user_id từ JWT
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing subject",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # 4. Tìm User trong Database
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user identity",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    # 5. User không tồn tại
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # 6. User bị khóa
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # 7. Trả User cho Endpoint
    return user