
from backend.app.models.account import Account, AccountCreate, AccountUpdate

from backend.app.repositories.base_repositories import AsyncBaseRepository, QueryMixin


class AccountRepository(AsyncBaseRepository[Account, AccountCreate, AccountUpdate], QueryMixin):
    """
    Репозиторий для работы с сущностью Account в асинхронной базе данных.

    Наследует методы базового репозитория для операций с Account и реализует интерфейс QueryMixin
    для выполнения дополнительных запросов.

    """

    def __init__(self):
        """
        Инициализирует репозиторий для работы с моделью Account.
        Вызывает конструктор базового класса для настройки сессий работы с данными.
        """
        super().__init__(Account)

