from typing import Optional

from .temp import Temp


class Reg(Temp):
    def __init__(self, id: int, name: str) -> None:
        # need to consider
        super().__init__(-id - 1)
        self.id = id
        self.name = name

        self.occupied = False
        self.used = False
        self.temp: Optional[Temp] = None

    def isUsed(self):
        return self.used

    def __str__(self) -> str:
        return self.name
