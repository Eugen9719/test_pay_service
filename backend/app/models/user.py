from pydantic import BaseModel, computed_field
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, max_length=255)
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    is_superuser: bool = Field(default=False)
    hashed_password: str

    # Связь один-ко-многим с Account
    accounts: List["Account"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )



class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: str | None = Field(None, max_length=255)
    first_name: str | None = None
    last_name: str | None = None
    is_superuser: bool | None = None
    password: str | None = None  # Новый пароль (опционально)


class UserRead(UserBase):
    id: int

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name or ''} {self.last_name or ''}".strip()