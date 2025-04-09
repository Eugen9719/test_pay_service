from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, Tuple, Any, Sequence

from pydantic import BaseModel
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateType = TypeVar("CreateType", bound=BaseModel)
UpdateType = TypeVar("UpdateType", bound=BaseModel)


# Интерфейс для базовых операций с репозиторием
class ICrudRepository(ABC, Generic[ModelType, CreateType, UpdateType]):
    @abstractmethod
    async def create(self, db: AsyncSession, schema: CreateType, **kwargs) -> ModelType:
        pass

    @abstractmethod
    async def update(self, db: AsyncSession, model: ModelType, schema: UpdateType | dict) -> ModelType:
        pass

    @abstractmethod
    async def get(self, db: AsyncSession, **kwargs) -> Optional[ModelType]:
        pass

    @abstractmethod
    async def remove(self, db: AsyncSession, **kwargs) -> Tuple[bool, Optional[ModelType]]:
        pass


class IQueryRepository(ABC, Generic[ModelType]):
    @abstractmethod
    async def get_or_404(self, db: AsyncSession, id: int, options: Optional[list[Any]] = None):
        pass

    @abstractmethod
    async def exist(self, db: AsyncSession, **kwargs) -> bool:
        pass

    @abstractmethod
    async def base_filter(self, db: AsyncSession, *filters, options=None):
        pass
