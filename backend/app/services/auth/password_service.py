from backend.app.abstractions.services import IPasswordService
from backend.core.security import pwd_context


class PasswordService(IPasswordService):
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
