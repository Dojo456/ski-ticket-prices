from models import PydanticCalendar
from abc import ABC, abstractmethod
from typing import Any, override
from models import *


class Template(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def make_request(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def parse_data(self, data: dict) -> PydanticCalendar:
        raise NotImplementedError
