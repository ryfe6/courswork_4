from abc import ABC, abstractmethod
from typing import Any


class Request(ABC):
    """Абстрактный класс для получения данных с сайта."""

    @abstractmethod
    def get_vacancies(self, *args: Any, **kwargs: Any) -> None:
        pass


class DataWrite:
    """Абстрактный класс для записи данных в файл."""

    @abstractmethod
    def data_write(self, *args: Any, **kwargs: Any) -> None:
        pass
