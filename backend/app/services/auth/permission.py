from fastapi import HTTPException
from starlette import status

from backend.app.models import User


class PermissionService:

    @staticmethod
    def verify_owner_account(model, user):
        if not model.user_id == user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Вы не можете просматривать чужой аккаунт")

    @staticmethod
    def verify_superuser(model: User) -> None:
        """Проверяет права суперпользователя"""
        if not model.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Требуются права администратора"
            )
