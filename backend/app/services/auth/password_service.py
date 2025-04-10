from backend.app.abstractions.services import IPasswordService
from backend.core.security import pwd_context


class PasswordService(IPasswordService):
    """Сервис для хэширования и проверки паролей пользователей."""

    def hash_password(self, password: str) -> str:
        """
        Хэширует пароль с использованием заданного контекста.

        :param password: Пароль в открытом виде, который нужно хэшировать.
        :return: str: Хэшированный пароль.
        """
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Проверяет, соответствует ли открытый пароль хэшированному.

        :param plain_password: Открытый пароль, который нужно проверить.
        :param hashed_password: Хэшированный пароль для проверки.
        :return: bool: True, если пароль совпадает, иначе False.
        """
        return pwd_context.verify(plain_password, hashed_password)

