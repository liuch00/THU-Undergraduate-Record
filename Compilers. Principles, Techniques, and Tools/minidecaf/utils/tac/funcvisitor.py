from __future__ import annotations

from typing import Union

from utils.label.funclabel import FuncLabel
from .context import Context
from .tacfunc import TACFunc
from .tacinstr import *
from .tacop import *
from .temp import Temp


class FuncVisitor:
    def __init__(self, entry: FuncLabel, numArgs: int, ctx: Context) -> None:
        self.ctx = ctx
        self.func = TACFunc(entry, numArgs)
        self.visitLabel(entry)
        self.nextTempId = 0

        self.continueLabelStack = []
        self.breakLabelStack = []

    # To get a fresh new temporary variable.
    def freshTemp(self) -> Temp:
        temp = Temp(self.nextTempId)
        self.nextTempId += 1
        return temp

    # To get a fresh new label (for jumping and branching, etc).
    def freshLabel(self) -> Label:
        return self.ctx.freshLabel()

    # To count how many temporary variables have been used.
    def getUsedTemp(self) -> int:
        return self.nextTempId

    # In fact, the following methods can be named 'appendXXX' rather than 'visitXXX'. E.g., by calling 'visitAssignment', you add an assignment instruction at the end of current function.
    def visitAssignment(self, dst: Temp, src: Temp) -> Temp:
        self.func.add(Assign(dst, src))
        return src

    def visitLoadImm4(self, value: Union[int, str]) -> Temp:
        temp = self.freshTemp()
        self.func.add(LoadImm4(temp, value))
        return temp

    def visitUnary(self, op: UnaryOp, operand: Temp) -> Temp:
        temp = self.freshTemp()
        self.func.add(Unary(op, temp, operand))
        return temp

    def visitUnarySelf(self, op: UnaryOp, operand: Temp) -> None:
        self.func.add(Unary(op, operand, operand))

    def visitBinary(self, op: BinaryOp, lhs: Temp, rhs: Temp) -> Temp:
        temp = self.freshTemp()
        if op == BinaryOp.EQ_HELP:
            self.func.add(Binary(BinaryOp.SUB, temp, lhs, rhs))
            self.func.add(Unary(UnaryOp.SEQZ, temp, temp))
        elif op == BinaryOp.NE_HELP:
            self.func.add(Binary(BinaryOp.SUB, temp, lhs, rhs))
            self.func.add(Unary(UnaryOp.SNEZ, temp, temp))
        elif op == BinaryOp.LE_HELP:
            self.func.add(Binary(BinaryOp.SGT, temp, lhs, rhs))
            self.func.add(Unary(UnaryOp.SEQZ, temp, temp))
        elif op == BinaryOp.GE_HELP:
            self.func.add(Binary(BinaryOp.SLT, temp, lhs, rhs))
            self.func.add(Unary(UnaryOp.SEQZ, temp, temp))
        else:
            self.func.add(Binary(op, temp, lhs, rhs))
        return temp

    def visitBinarySelf(self, op: BinaryOp, lhs: Temp, rhs: Temp) -> None:
        self.func.add(Binary(op, lhs, lhs, rhs))

    def visitBranch(self, target: Label) -> None:
        self.func.add(Branch(target))

    def visitCondBranch(self, op: CondBranchOp, cond: Temp, target: Label) -> None:
        self.func.add(CondBranch(op, cond, target))

    def visitReturn(self, value: Optional[Temp]) -> None:
        self.func.add(Return(value))

    def visitLabel(self, label: Label) -> None:
        self.func.add(Mark(label))

    def visitMemo(self, content: str) -> None:
        self.func.add(Memo(content))

    def visitRaw(self, instr: TACInstr) -> None:
        self.func.add(instr)

    def visitEnd(self) -> None:
        if (len(self.func.instrSeq) == 0) or (not self.func.instrSeq[-1].isReturn()):
            self.func.add(Return(None))
        self.func.tempUsed = self.getUsedTemp()
        self.ctx.funcs.append(self.func)

    # To open a new loop (for break/continue statements)
    def openLoop(self, breakLabel: Label, continueLabel: Label) -> None:
        self.breakLabelStack.append(breakLabel)
        self.continueLabelStack.append(continueLabel)

    # To close the current loop.
    def closeLoop(self) -> None:
        self.breakLabelStack.pop()
        self.continueLabelStack.pop()

    # To get the label for 'break' in the current loop.
    def getBreakLabel(self) -> Label:
        return self.breakLabelStack[-1]

    # To get the label for 'continue' in the current loop.
    def getContinueLabel(self) -> Label:
        return self.continueLabelStack[-1]

    def visitSetupPara(self, src: Temp, index: int) -> None:
        self.func.add(SetupPara(src, index))

    def visitCall(self, target: Label, dst: Temp, para_cnt: int) -> Temp:
        self.func.add(Call(target, dst, para_cnt))
        return dst

    def visitAlloc(self, dst: Temp, size: int) -> None:
        self.func.add(Alloc(dst, size))

    def visitLoad(self, dst: Temp, base: Temp, offset: int) -> None:
        self.func.add(Load(dst, base, offset))

    def visitStore(self, src: Temp, base: Temp, offset: int) -> None:
        self.func.add(Store(src, base, offset))

    def visitLoadAddress(self, dst: Temp, name: str) -> None:
        self.func.add(LoadAddress(name, dst))
