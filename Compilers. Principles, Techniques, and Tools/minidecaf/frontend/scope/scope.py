from enum import Enum, auto, unique

from frontend.symbol.symbol import Symbol

"""
A scope stores the mapping from names to symbols. There are two kinds of scopes:
    global scope: stores global variables and functions
    local scope: stores local variables of a code block
"""


@unique
class ScopeKind(Enum):
    GLOBAL = auto()
    LOCAL = auto()


class Scope:
    def __init__(self, kind: ScopeKind) -> None:
        self.kind = kind
        self.symbols = {}

    # To check if a symbol is declared in the scope.
    def containsKey(self, key: str) -> bool:
        return key in self.symbols

    # To get a symbol via its name.
    def get(self, key: str) -> Symbol:
        return self.symbols[key]

    # To declare a symbol.
    def declare(self, symbol: Symbol) -> None:
        self.symbols[symbol.name] = symbol
        symbol.setDomain(self)

    # To check if this is a global scope.
    def isGlobalScope(self) -> bool:
        return False
