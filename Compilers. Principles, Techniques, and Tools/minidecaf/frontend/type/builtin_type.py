import utils.riscv as riscv

from .type import DecafType

"""
Built-in type: int
"""


class BuiltinType(DecafType):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def is_base(self):
        return True

    @property
    def size(self) -> int:
        return riscv.WORD_SIZE

    def __eq__(self, o: object) -> bool:
        if isinstance(o, BuiltinType) and self.name == o.name:
            return True
        return False

    def __str__(self) -> str:
        return self.name


INT = BuiltinType("int")
