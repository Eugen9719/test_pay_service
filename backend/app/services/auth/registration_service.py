from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.app.abstractions.services import IPasswordService
from backend.app.models.user import User, UserCreate
from backend.app.repositories.user_repositories import UserRepository
from backend.app.services.auth.permission import PermissionService


class RegistrationService:
    """Сервис регистрации пользователей"""

    def __init__(self, user_repository: UserRepository, pass_service: IPasswordService,
                 permission: PermissionService, ):
        self.user_repository = user_repository
        self.pass_service = pass_service
        self.permission = permission

    async def create_user(self, schema: UserCreate, db: AsyncSession, current_user: User):
        self.permission.verify_superuser(current_user)

        existing_user = await self.user_repository.get_by_email(db, email=schema.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
        hashed_password = self.pass_service.hash_password(schema.password)
        user = await self.user_repository.create_user(db, schema=schema, hashed_password=hashed_password)
        return user
