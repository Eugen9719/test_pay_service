from backend.app.models.payment import Payment, PaymentCreate, PaymentUpdate
from backend.app.repositories.base_repositories import AsyncBaseRepository, QueryMixin


class PaymentRepository(AsyncBaseRepository[Payment, PaymentCreate, PaymentUpdate], QueryMixin):
    """
    Репозиторий для работы с сущностью Payment в асинхронной базе данных.

    Наследует методы базового репозитория для операций с сущностью Payment и реализует интерфейс QueryMixin
    для выполнения дополнительных запросов.
    """

    def __init__(self):
        """
        Инициализирует репозиторий для работы с моделью Payment.
        Вызывает конструктор базового класса для настройки сессий работы с данными.
        """
        super().__init__(Payment)
