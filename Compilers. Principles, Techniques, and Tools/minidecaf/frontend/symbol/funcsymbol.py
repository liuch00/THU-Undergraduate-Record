from __future__ import annotations

from frontend.scope.scope import Scope
from .symbol import *

"""
Function symbol, representing a function definition.
"""


class FuncSymbol(Symbol):
    def __init__(self, isDecl: bool, name: str, type: DecafType, scope: Scope) -> None:
        super().__init__(name, type)
        self.scope = scope
        self.para_type = []
        self.isDecl = isDecl

    def __str__(self) -> str:
        return "function %s : %s" % (self.name, str(self.type))

    @property
    def isFunc(self) -> bool:
        return True

    # To add the type of a parameter. In fact, parameters can only be 'int' in MiniDecaf.
    def addParaType(self, type: DecafType) -> None:
        self.para_type.append(type)

    # To get the parameter number of a function symbol.
    @property
    def parameterNum(self) -> int:
        return len(self.para_type)

    # To get the parameters' type.
    def getParaType(self, id: int) -> DecafType:
        return self.para_type[id]
