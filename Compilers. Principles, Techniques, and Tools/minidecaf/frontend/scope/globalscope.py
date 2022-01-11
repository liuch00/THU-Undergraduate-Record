from frontend.symbol.symbol import Symbol

from .scope import Scope, ScopeKind

"""
Global scope stores all symbols of global variables and functions.
"""


class GlobalScopeType(Scope):
    def __init__(self) -> None:
        super().__init__(ScopeKind.GLOBAL)
        self.definedGlobalVar = {}

    def isGlobalScope(self) -> bool:
        return True

    def define(self, symbol: Symbol) -> None:
        self.definedGlobalVar[symbol.name] = True

    def isDefined(self, symbol: Symbol) -> bool:
        return symbol.name in self.definedGlobalVar


"""
You can access global scope via GlobalScope. This should be the only instance of GlobalScopeType.
"""
GlobalScope = GlobalScopeType()
