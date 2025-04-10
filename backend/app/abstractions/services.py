from abc import ABC, abstractmethod


# Интерфейс для работы с паролями
class IPasswordService(ABC):
    """
       Интерфейс для сервиса работы с паролями.

       Определяет методы для хеширования паролей и проверки их соответствия с сохранёнными хешами.

       Используется для безопасной работы с паролями пользователей.
       """

    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass
