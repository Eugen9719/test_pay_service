from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession
from backend.app.models import User
from backend.app.models.schemas import Msg
from backend.app.models.user import UserUpdate
from backend.app.repositories.user_repositories import UserRepository
from backend.app.services.auth.password_service import PasswordService
from backend.app.services.auth.permission import PermissionService


class UserService:
    """Сервис управления пользователями"""

    def __init__(self, user_repository: UserRepository, permission: PermissionService, pass_service: PasswordService):
        """
        Инициализация сервиса управления пользователями.

        :param user_repository: Репозиторий для работы с пользователями.
        :param permission: Сервис для проверки прав доступа.
        :param pass_service: Сервис для работы с паролями.
        """
        self.user_repository = user_repository
        self.permission = permission
        self.pass_service = pass_service

    async def update_user(self, db: AsyncSession, schema: UserUpdate, user_id: int, current_user: User) -> User:
        """
        Обновляет данные пользователя, включая проверку уникальности email.

        :param db: Асинхронная сессия базы данных.
        :param schema: Данные, на основе которых обновляются сведения пользователя.
        :param user_id: ID пользователя, которого нужно обновить.
        :param current_user: Текущий пользователь, выполняющий операцию.
        :return: Обновлённый объект пользователя.
        :raises HTTPException: Если текущий пользователь не имеет прав суперпользователя.
        """
        self.permission.verify_superuser(current_user)
        existing_user = await self.user_repository.get_or_404(db, id=user_id)
        if schema.password:
            existing_user.hashed_password = self.pass_service.hash_password(schema.password)
        return await self.user_repository.update(db=db, model=existing_user,
                                                 schema=schema.model_dump(exclude_unset=True, exclude={"password"}))

    async def delete_user(self, db: AsyncSession, current_user: User, user_id: int) -> Msg:
        """
        Удаляет пользователя из базы данных.

        :param db: Асинхронная сессия базы данных.
        :param current_user: Текущий пользователь, выполняющий операцию.
        :param user_id: ID пользователя, которого нужно удалить.
        :return: Сообщение о статусе операции.
        :raises HTTPException: Если текущий пользователь не имеет прав суперпользователя.
        """
        self.permission.verify_superuser(current_user)
        target_user = await self.user_repository.get_or_404(db, id=user_id)
        await self.user_repository.delete_user(db=db, user_id=target_user.id)
        return Msg(msg="Пользователь удален успешно")

    async def get_user_me(self, db: AsyncSession, current_user: User):
        """
        Получает информацию о текущем пользователе, включая его счета.

        :param db: Асинхронная сессия базы данных.
        :param current_user: Текущий пользователь.
        :return: Данные текущего пользователя.
        """
        return await self.user_repository.get_or_404(db=db, id=current_user.id, options=[selectinload(User.accounts)])

    async def get_users(self, db: AsyncSession, current_user: User):
        """
        Получает всех пользователей, кроме суперпользователей.

        :param db: Асинхронная сессия базы данных.
        :param current_user: Текущий пользователь, выполняющий операцию.
        :return: Список пользователей, исключая суперпользователей.
        :raises HTTPException: Если текущий пользователь не имеет прав суперпользователя.
        """
        self.permission.verify_superuser(current_user)
        return await self.user_repository.base_filter(db,  User.is_superuser==False, options=[selectinload(User.accounts)])

