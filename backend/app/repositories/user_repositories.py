from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

from backend.app.models import User
from backend.app.models.user import UserCreate, UserUpdate

from backend.app.repositories.base_repositories import AsyncBaseRepository, QueryMixin


class UserRepository(AsyncBaseRepository[User, UserCreate, UserUpdate], QueryMixin):
    """
    Репозиторий для работы с сущностью User в асинхронной базе данных.

    Наследует методы базового репозитория для операций с сущностью User и реализует интерфейс QueryMixin
    для выполнения дополнительных запросов.
    """

    def __init__(self):
        """
        Инициализирует репозиторий для работы с моделью User.
        Вызывает конструктор базового класса для настройки сессий работы с данными.
        """
        super().__init__(User)


    async def create_user(self, db: AsyncSession, schema: UserCreate, hashed_password) -> User:
        """Создание нового пользователя"""
        return await super().create(db, schema, hashed_password=hashed_password)

    async def update_user(self, db: AsyncSession, schema: UserUpdate, model: User) -> User:
        """Обновление данных пользователя"""
        return await super().update(db=db, model=model, schema=schema)

    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        """Получение пользователя по email."""
        return await self.get(db, email=email)

    async def delete_user(self, db: AsyncSession, user_id: int) -> tuple[bool, SQLModel | None | Any]:
        """Удаление пользователя"""
        return await super().remove(db=db, id=user_id)
