import uuid
from decimal import Decimal
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession
from backend.app.models import User
from backend.app.models.account import Account
from backend.app.repositories.account_repositories import AccountRepository
from backend.app.services.auth.permission import PermissionService


class AccountService:
    def __init__(self, account_repository: AccountRepository, permissions: PermissionService):
        self.account_repository = account_repository
        self.permissions = permissions

    async def create_account(self, db: AsyncSession, current_user: User) -> Account:
        # Генерируем уникальный номер счета
        account_number = f"ACC-{uuid.uuid4().hex[:8].upper()}"  # Пример: "ACC-A1B2C3D4"

        account = Account(
            account_number=account_number,
            user_id=current_user.id,
            balance=Decimal('0.00')  # Начальный баланс
        )

        account = await self.account_repository.save_db(db, account)
        return account

    async def get_account(self, db: AsyncSession, account_id: int, current_user: User):
        account = await self.account_repository.get_or_404(db, id=account_id, options=[selectinload(Account.payments)])
        self.permissions.verify_owner_account(account, current_user)
        return account