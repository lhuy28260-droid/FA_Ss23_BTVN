from fastapi import Depends, HTTPException, status

from dependencies.authentication import get_current_user
from models.models import User


def require_role(required_role: str):

    def role_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:

        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )

        return current_user

    return role_checker


def require_admin(
    current_user: User = Depends(
        require_role("admin")
    )
) -> User:

    return current_user