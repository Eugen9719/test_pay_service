from backend.app.models import Account
from backend.app.models.account import AccountCreate, AccountUpdate

from backend.app.repositories.base_repositories import AsyncBaseRepository, QueryMixin


class AccountRepository(AsyncBaseRepository[Account, AccountCreate, AccountUpdate], QueryMixin):
    def __init__(self):
        super().__init__(Account)
