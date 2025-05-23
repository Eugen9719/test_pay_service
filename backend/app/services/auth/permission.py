from fastapi import HTTPException
from starlette import status

from backend.app.models import User


class PermissionService:
    """Сервис для проверки прав доступа пользователей."""

    @staticmethod
    def verify_owner_account(model, user):
        """
        Проверяет, является ли пользователь владельцем аккаунта.

        :param model: Модель аккаунта, для которого проводится проверка.
        :param user: Пользователь, чьи права доступа проверяются.
        :raises HTTPException: Если пользователь не является владельцем аккаунта.
        """
        if not model.user_id == user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Вы не можете просматривать чужой аккаунт")

    @staticmethod
    def verify_superuser(model: User) -> None:
        """
        Проверяет, имеет ли пользователь права суперпользователя.

        :param model: Пользователь, чьи права проверяются.
        :raises HTTPException: Если пользователь не является суперпользователем.
        """
        if not model.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Требуются права администратора"
            )
