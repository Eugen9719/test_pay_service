from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.app.abstractions.services import IPasswordService
from backend.app.models.user import User, UserCreate
from backend.app.repositories.user_repositories import UserRepository
from backend.app.services.auth.permission import PermissionService


class RegistrationService:
    """Сервис регистрации пользователей"""

    def __init__(self, user_repository: UserRepository, pass_service: IPasswordService,
                 permission: PermissionService):
        """
        Инициализация сервиса регистрации пользователей.

        :param user_repository: Репозиторий для работы с пользователями.
        :param pass_service: Сервис для хеширования паролей.
        :param permission: Сервис для проверки прав доступа.
        """
        self.user_repository = user_repository
        self.pass_service = pass_service
        self.permission = permission

    async def create_user(self, schema: UserCreate, db: AsyncSession, current_user: User):
        """
        Регистрирует нового пользователя.

        :param schema: Данные для создания нового пользователя.
        :param db: Асинхронная сессия базы данных.
        :param current_user: Текущий пользователь, выполняющий операцию.
        :return: Созданный объект пользователя.
        :raises HTTPException: Если пользователь с таким email уже существует.
        :raises HTTPException: Если текущий пользователь не имеет прав суперпользователя.
        """
        self.permission.verify_superuser(current_user)

        # Проверка, если пользователь с таким email уже зарегистрирован
        existing_user = await self.user_repository.get_by_email(db, email=schema.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

        hashed_password = self.pass_service.hash_password(schema.password)
        user = await self.user_repository.create_user(db, schema=schema, hashed_password=hashed_password)

        return user
