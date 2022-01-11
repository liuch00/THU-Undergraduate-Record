from typing import Optional

from .tacfunc import TACFunc


class GlobalVarInfo:
    def __init__(self, name: str, size: int, init: Optional[int]):
        self.name = name
        self.size = size
        self.init = init


class TACProg:
    def __init__(self, funcs: list[TACFunc], glob_vars: list[GlobalVarInfo]) -> None:
        self.funcs = funcs
        self.glob_vars = glob_vars

    def printTo(self) -> None:
        for func in self.funcs:
            func.printTo()
