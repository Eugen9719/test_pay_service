from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.payment import PaymentCreate
from backend.app.models.schemas import WebhookRequest
from backend.app.services.helpers import verify_signature


class PaymentService:
    def __init__(self, payment_repository, account_repository, user_repository, permissions, account_service):
        """
        Сервис для обработки платёжных транзакций.

        :param payment_repository: Репозиторий для работы с платежами.
        :param account_repository: Репозиторий для работы со счетами.
        :param user_repository: Репозиторий для работы с пользователями.
        :param permissions: Сервис проверки прав доступа.
        :param account_service: Сервис управления счетами.
        """
        self.payment_repository = payment_repository
        self.account_repository = account_repository
        self.user_repository = user_repository
        self.permissions = permissions
        self.account_service = account_service

    async def _validate_payment_data(self, db, data):
        """
        Проверяет корректность входящих платёжных данных.

        :param db: Сессия базы данных.
        :param data: Вебхук-запрос от платёжной системы.
        :raises HTTPException: Если подпись некорректна или транзакция уже существует.
        """
        if data.signature != verify_signature(data):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid signature")

        if await self.payment_repository.exist(db, transaction_id=data.transaction_id):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Транзакция {data.transaction_id} уже существует")

    async def _get_or_create_account(self, db, data):
        """
        Получает счёт по ID или создаёт новый, если не найден.

        :param db: Сессия базы данных.
        :param data: Вебхук-запрос от платёжной системы.
        :return: Счёт, связанный с пользователем.
        :raises HTTPException: Если id счёта найдено, но принадлежит другому пользователю.
        """
        account = await self.account_repository.get(db, id=data.account_id)
        if account and account.user_id != data.user_id:
            raise HTTPException(400, "Счет принадлежит другому пользователю")
        if not account:
            user = await self.user_repository.get_or_404(db, id=data.user_id)
            account = await self.account_service.create_account(db, user)
        return account

    async def process_payment(self, db: AsyncSession, data: WebhookRequest):
        """
        Обрабатывает платёж, обновляет баланс счёта и сохраняет транзакцию.

        :param db: Асинхронная сессия базы данных.
        :param data: Данные, полученные из вебхука платёжной системы.
        :return: dict: Статус операции и обновлённый баланс счёта.
        :raises HTTPException: При ошибках валидации данных или доступе к счёту.
        """
        await self._validate_payment_data(db, data)
        account = await self._get_or_create_account(db, data)

        await self.payment_repository.create(db, PaymentCreate(
            transaction_id=data.transaction_id,
            account_id=account.id,
            amount=data.amount,
        ))

        account.balance += Decimal(str(data.amount))
        await self.account_repository.save_db(db, account)
        return {"status": "success", "new_balance": account.balance}
