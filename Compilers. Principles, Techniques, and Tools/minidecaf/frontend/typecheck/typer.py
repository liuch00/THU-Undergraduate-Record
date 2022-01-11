from frontend.ast.tree import *
from frontend.ast.visitor import Visitor
from frontend.scope.scopestack import ScopeStack

"""
The typer phase: type check abstract syntax tree.
"""


class Typer(Visitor[ScopeStack, None]):
    def __init__(self) -> None:
        pass

    # Entry of this phase
    def transform(self, program: Program) -> Program:
        return program
