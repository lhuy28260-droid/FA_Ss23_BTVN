import os
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from dotenv import load_dotenv

# ==========================================
# LOAD CONFIGURATION
# ==========================================

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "30"
    )
)


# Kiểm tra SECRET_KEY
if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY is not configured"
    )


# ==========================================
# PASSWORD
# ==========================================

def hash_password(password: str) -> str:
    """
    Hash password trước khi lưu Database.
    """

    password_bytes = password.encode("utf-8")

    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed_password.decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Kiểm tra password người dùng nhập
    có khớp password hash trong Database hay không.
    """

    plain_password_bytes = plain_password.encode(
        "utf-8"
    )

    hashed_password_bytes = hashed_password.encode(
        "utf-8"
    )

    return bcrypt.checkpw(
        plain_password_bytes,
        hashed_password_bytes
    )


# ==========================================
# JWT
# ==========================================

def create_access_token(
    user_id: str,
    role: str
) -> str:
    """
    Tạo JWT cho User sau khi đăng nhập thành công.
    """

    expire_time = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": user_id,
        "role": role,
        "exp": expire_time
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def decode_access_token(token: str) -> dict:
    """
    Giải mã và kiểm tra JWT.

    Nếu token không hợp lệ hoặc hết hạn,
    jwt.decode() sẽ phát sinh exception.
    """

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return payload