from __future__ import annotations

from abc import ABC, abstractmethod

from frontend.type.type import DecafType

"""
A symbol is created when a variable/function definition is identified.

Symbols are stored in the symbol table of a scope and referred by other expressions/statements.
"""


class Symbol(ABC):
    def __init__(self, name: str, type: DecafType) -> None:
        self.name = name
        self.type = type

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError()

    # To set which scope is this symbol belonged to.
    def setDomain(self, scope) -> None:
        self.definedIn = scope

    # To get which scope is this symbol defined in.
    @property
    def domain(self):
        return self.definedIn

    # To check if this is a function symbol.
    @property
    def isFunc(self) -> bool:
        return False
