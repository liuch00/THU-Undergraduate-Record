from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

"""
There are two kinds of types:
    built-in types: int
    array types: array of int (may be multi-dimensional)
"""


class DecafType(ABC):
    def is_base(self):
        return False

    def is_array(self):
        return False

    @property
    def indexed(self) -> Optional[DecafType]:
        return None

    def can_cast(self, to: DecafType) -> bool:
        return isinstance(to, type(self))

    @property
    @abstractmethod
    def size(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, o: object) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError
