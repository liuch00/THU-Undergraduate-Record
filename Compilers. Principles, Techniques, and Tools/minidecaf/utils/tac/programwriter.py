from __future__ import annotations

from utils.label.funclabel import *
from .context import Context
from .funcvisitor import FuncVisitor
from .tacprog import TACProg, GlobalVarInfo


class ProgramWriter:
    def __init__(self, funcs: list[str], glob_var: list[GlobalVarInfo]) -> None:
        self.funcs = []
        self.glob_var = glob_var
        self.ctx = Context()
        for func in funcs:
            self.funcs.append(func)
            self.ctx.putFuncLabel(func)

    def visitMainFunc(self) -> FuncVisitor:
        entry = MAIN_LABEL
        return FuncVisitor(entry, 0, self.ctx)

    def visitFunc(self, name: str, numArgs: int) -> FuncVisitor:
        entry = self.ctx.getFuncLabel(name)
        return FuncVisitor(entry, numArgs, self.ctx)

    def visitEnd(self) -> TACProg:
        return TACProg(self.ctx.funcs, self.glob_var)
