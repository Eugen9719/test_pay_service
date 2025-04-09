from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel
from sqlalchemy import Column, Numeric
from sqlmodel import SQLModel, Field, Relationship

from backend.app.models.payment import PaymentRead


class Account(SQLModel, table=True):
    __tablename__ = 'account'
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    account_number: str = Field(unique=True, index=True)
    user_id: int = Field(foreign_key="user.id", description="ID связанного пользователя")
    balance: Decimal = Field(
        default=Decimal('0.00'),
        sa_column=Column(Numeric(precision=10, scale=2))
    )

    # Связь многие-к-одному с User
    user: "User" = Relationship(back_populates="accounts")
    # Связь один-ко-многим с Payment
    payments: List["Payment"] = Relationship(
        back_populates="account",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class AccountCreate(BaseModel):
    pass


class AccountUpdate(BaseModel):
    pass


class AccountRead(BaseModel):
    id: int
    account_number: str
    balance: float





class AccountReadWithPayments(AccountRead):
    payments: List[PaymentRead]