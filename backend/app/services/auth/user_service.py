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
        self.user_repository = user_repository
        self.permission = permission
        self.pass_service = pass_service

    async def update_user(self, db: AsyncSession, schema: UserUpdate, user_id: int, current_user: User) -> User:
        """Обновление данных пользователя с проверкой уникальности email."""
        self.permission.verify_superuser(current_user)
        existing_user = await self.user_repository.get_or_404(db, id=user_id)
        if schema.password:
            existing_user.hashed_password = self.pass_service.hash_password(schema.password)
        return await self.user_repository.update(db=db, model=existing_user,
                                                 schema=schema.model_dump(exclude_unset=True, exclude={"password"}))

    async def delete_user(self, db: AsyncSession, current_user: User, user_id: int) -> Msg:
        self.permission.verify_superuser(current_user)
        target_user = await self.user_repository.get_or_404(db, id=user_id)
        await self.user_repository.delete_user(db=db, user_id=target_user.id)
        return Msg(msg="Пользователь удален успешно")

    async def get_user_me(self, db: AsyncSession, current_user: User):
        return await self.user_repository.get_or_404(db=db, id=current_user.id, options=[selectinload(User.accounts)])

    async def get_users(self, db: AsyncSession, current_user: User):
        self.permission.verify_superuser(current_user)
        return await self.user_repository.base_filter(db,  User.is_superuser==False, options=[selectinload(User.accounts)])
