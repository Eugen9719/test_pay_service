from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, Tuple, Any

from pydantic import BaseModel
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateType = TypeVar("CreateType", bound=BaseModel)
UpdateType = TypeVar("UpdateType", bound=BaseModel)


# Интерфейс для базовых операций с репозиторием
class ICrudRepository(ABC, Generic[ModelType, CreateType, UpdateType]):
    """
    Интерфейс для репозитория с базовыми CRUD операциями для работы с моделями данных.

    Определяет методы для создания, обновления, получения и удаления данных.
    """

    @abstractmethod
    async def create(self, db: AsyncSession, schema: CreateType, **kwargs) -> ModelType:
        """
        Создаёт новый объект в базе данных.

        :param db: Асинхронная сессия базы данных.
        :param schema: Данные для создания объекта.
        :param kwargs: Дополнительные параметры.
        :return: Объект модели, созданный в базе данных.
        """
        pass

    @abstractmethod
    async def update(self, db: AsyncSession, model: ModelType, schema: UpdateType | dict) -> ModelType:
        """
        Обновляет существующий объект в базе данных.

        :param db: Асинхронная сессия базы данных.
        :param model: Объект модели для обновления.
        :param schema: Данные для обновления модели (или словарь с полями).
        :return: Обновлённый объект модели.
        """
        pass

    @abstractmethod
    async def get(self, db: AsyncSession, **kwargs) -> Optional[ModelType]:
        """
        Получает объект модели из базы данных по указанным фильтрам.

        :param db: Асинхронная сессия базы данных.
        :param kwargs: Параметры для фильтрации.
        :return: Объект модели или None, если объект не найден.
        """
        pass

    @abstractmethod
    async def remove(self, db: AsyncSession, **kwargs) -> Tuple[bool, Optional[ModelType]]:
        """
        Удаляет объект из базы данных.

        :param db: Асинхронная сессия базы данных.
        :param kwargs: Параметры для удаления.
        :return: Кортеж с флагом успеха и удалённым объектом.
        """
        pass



class IQueryRepository(ABC, Generic[ModelType]):
    """
    Интерфейс для репозитория с методами запросов, включая поиск и фильтрацию данных.

    :param ModelType: Тип модели, с которой работает репозиторий.

    Определяет методы для получения объектов по идентификатору, проверку существования объекта
    и выполнение фильтрации.
    """

    @abstractmethod
    async def get_or_404(self, db: AsyncSession, id: int, options: Optional[list[Any]] = None):
        """
        Получает объект по идентификатору или вызывает исключение 404, если объект не найден.

        :param db: Асинхронная сессия базы данных.
        :param id: Идентификатор объекта.
        :param options: Дополнительные параметры для выполнения запроса.
        :return: Объект модели, если найден.
        :raises HTTPException: Если объект не найден, выбрасывается ошибка 404.
        """
        pass

    @abstractmethod
    async def exist(self, db: AsyncSession, **kwargs) -> bool:
        """
        Проверяет существование объекта в базе данных по заданным параметрам.

        :param db: Асинхронная сессия базы данных.
        :param kwargs: Параметры для фильтрации.
        :return: True, если объект существует, иначе False.
        """
        pass

    @abstractmethod
    async def base_filter(self, db: AsyncSession, *filters, options=None):
        """
        Выполняет базовую фильтрацию объектов по заданным фильтрам.

        :param db: Асинхронная сессия базы данных.
        :param filters: Фильтры для выполнения запроса.
        :param options: Дополнительные параметры для запроса.
        :return: Список объектов, соответствующих фильтрам.
        """
        pass

