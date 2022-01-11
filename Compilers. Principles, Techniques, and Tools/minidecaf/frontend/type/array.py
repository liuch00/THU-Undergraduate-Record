from __future__ import annotations

from utils.error import DecafBadArraySizeError
from .type import DecafType

"""
Array type is represented in a recursive form.

An array type consists of two parts: base type and length.

Some examples:
    ArrayType.multidim(INT, 1, 2, 3) == int[1][2][3]
    ArrayType(ArrayType(INT, 1), 2) == int[2][1]
    a: int[1][2]; type(a[0]) == int[2]
"""


class ArrayType(DecafType):
    def __init__(self, base: DecafType, length: int) -> None:
        super().__init__()
        self.base = base
        self.length = length
        if length <= 0:
            raise DecafBadArraySizeError

    def is_array(self):
        return True

    @property
    def indexed(self) -> DecafType:
        return self.base

    @property
    def _indexes(self) -> str:
        if isinstance(self.base, ArrayType):
            return f"[{self.length}]{self.base._indexes}"
        else:
            return f"[{self.length}]"

    @property
    def size(self) -> int:
        "To get the full size of an array, e.g. size(int[2][3]) == 2 * 3 * WORD_SIZE."
        return self.length * self.base.size

    @property
    def full_indexed(self) -> DecafType:
        "To get the ultimate type of an array, e.g. full_indexed(int[2][3]) == int."
        return self.base.full_indexed if isinstance(self.base, ArrayType) else self.base

    @property
    def dim(self) -> int:
        "To get the dimension of an array."
        return self.base.dim + 1 if isinstance(self.base, ArrayType) else 1

    def __eq__(self, o: object) -> bool:
        if (
                isinstance(o, type(self))
                and o.length == self.length
                and o.base == self.base
        ):
            return True
        else:
            return False

    def __str__(self) -> str:
        return f"{self.full_indexed}{self._indexes}"

    @classmethod
    def multidim(cls, base: DecafType, *dims: int) -> ArrayType:
        "To quickly generate a high-dimension array."
        if dims:
            return cls(cls.multidim(base, *dims[1:]), dims[0])
        else:
            return base  # type: ignore
