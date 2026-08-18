from sqlalchemy.orm import Session

from models.models import User
from schemas.schemas import LoginRequest
from security import (
    create_access_token,
    verify_password,
)


def login_user(
    db: Session,
    login_data: LoginRequest
) -> str:

    # 1. Tìm User theo username
    user = (
        db.query(User)
        .filter(User.username == login_data.username)
        .first()
    )

    # 2. User không tồn tại
    if not user:
        raise ValueError("Invalid username or password")

    # 3. Kiểm tra tài khoản có đang hoạt động không
    if not user.is_active:
        raise ValueError("User account is inactive")

    # 4. Kiểm tra password
    password_valid = verify_password(
        login_data.password,
        user.password_hash
    )

    if not password_valid:
        raise ValueError("Invalid username or password")

    # 5. Tạo JWT
    access_token = create_access_token(
        user_id=str(user.id),
        role=user.role
    )

    # 6. Trả JWT về Router
    return access_token