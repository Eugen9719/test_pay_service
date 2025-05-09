from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from backend.app.abstractions.services import IPasswordService
from backend.app.models import User
from backend.app.repositories.user_repositories import UserRepository


class UserAuthentication:
    """Сервис аутентификации пользователей."""

    def __init__(self, pass_service: IPasswordService, user_repository: UserRepository):
        """
        Инициализирует сервис аутентификации с необходимыми зависимостями.

        :param pass_service: Сервис для хэширования и проверки паролей.
        :param user_repository: Репозиторий для работы с данными пользователей.
        """
        self.pass_service = pass_service
        self.user_repository = user_repository

    async def authenticate(self, db: AsyncSession, email: str, password: str) -> Optional[User]:
        """
        Аутентифицирует пользователя по email и паролю.

        :param db: Асинхронная сессия базы данных.
        :param email: Электронная почта пользователя.
        :param password: Пароль пользователя.
        :return: Optional[User]: Возвращает пользователя, если аутентификация прошла успешно, иначе None.
        """
        user = await self.user_repository.get_by_email(db, email=email)
        if not user or not self.pass_service.verify_password(password, user.hashed_password):
            return None
        return user
