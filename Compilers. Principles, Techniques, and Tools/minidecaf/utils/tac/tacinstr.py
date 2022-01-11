from typing import Optional

from utils.label.label import Label
from utils.tac.nativeinstr import NativeInstr
from utils.tac.reg import Reg
from .tacop import *
from .tacvisitor import TACVisitor
from .temp import Temp


class TACInstr:
    def __init__(
            self,
            kind: InstrKind,
            dsts: list[Temp],
            srcs: list[Temp],
            label: Optional[Label],
    ) -> None:
        self.kind = kind
        self.dsts = dsts.copy()
        self.srcs = srcs.copy()
        self.label = label

    def getRead(self) -> list[int]:
        return [src.index for src in self.srcs]

    def getWritten(self) -> list[int]:
        return [dst.index for dst in self.dsts]

    def isLabel(self) -> bool:
        return self.kind is InstrKind.LABEL

    def isSequential(self) -> bool:
        return self.kind == InstrKind.SEQ

    def isReturn(self) -> bool:
        return self.kind == InstrKind.RET

    def toNative(self, dstRegs: list[Reg], srcRegs: list[Reg]) -> NativeInstr:
        oldDsts = dstRegs
        oldSrcs = srcRegs
        self.dsts = dstRegs
        self.srcs = srcRegs
        instrString = self.__str__()
        newInstr = NativeInstr(self.kind, dstRegs, srcRegs, self.label, instrString)
        self.dsts = oldDsts
        self.srcs = oldSrcs
        return newInstr

    def accept(self, v: TACVisitor) -> None:
        pass


# Assignment instruction.
class Assign(TACInstr):
    def __init__(self, dst: Temp, src: Temp) -> None:
        super().__init__(InstrKind.SEQ, [dst], [src], None)
        self.dst = dst
        self.src = src

    def __str__(self) -> str:
        return "%s = %s" % (self.dst, self.src)

    def accept(self, v: TACVisitor) -> None:
        v.visitAssign(self)


# Loading an immediate 32-bit constant.
class LoadImm4(TACInstr):
    def __init__(self, dst: Temp, value: int) -> None:
        super().__init__(InstrKind.SEQ, [dst], [], None)
        self.dst = dst
        self.value = value

    def __str__(self) -> str:
        return "%s = %d" % (self.dst, self.value)

    def accept(self, v: TACVisitor) -> None:
        v.visitLoadImm4(self)


# Unary operations.
class Unary(TACInstr):
    def __init__(self, op: UnaryOp, dst: Temp, operand: Temp) -> None:
        super().__init__(InstrKind.SEQ, [dst], [operand], None)
        self.op = op
        self.dst = dst
        self.operand = operand

    def __str__(self) -> str:
        return "%s = %s %s" % (
            self.dst,
            ("-" if (self.op == UnaryOp.NEG) else "!"),
            self.operand,
        )

    def accept(self, v: TACVisitor) -> None:
        v.visitUnary(self)


# Binary Operations.
class Binary(TACInstr):
    def __init__(self, op: BinaryOp, dst: Temp, lhs: Temp, rhs: Temp) -> None:
        super().__init__(InstrKind.SEQ, [dst], [lhs, rhs], None)
        self.op = op
        self.dst = dst
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        opStr = {
            BinaryOp.ADD: "+",
            BinaryOp.SUB: "-",
            BinaryOp.MUL: "*",
            BinaryOp.DIV: "/",
            BinaryOp.REM: "%",
            BinaryOp.EQU: "==",
            BinaryOp.NEQ: "!=",
            BinaryOp.SLT: "<",
            BinaryOp.LEQ: "<=",
            BinaryOp.SGT: ">",
            BinaryOp.GEQ: ">=",
            BinaryOp.AND: "&&",
            BinaryOp.OR: "||",
        }[self.op]
        return "%s = (%s %s %s)" % (self.dst, self.lhs, opStr, self.rhs)

    def accept(self, v: TACVisitor) -> None:
        v.visitBinary(self)


# Branching instruction.
class Branch(TACInstr):
    def __init__(self, target: Label) -> None:
        super().__init__(InstrKind.JMP, [], [], target)
        self.target = target

    def __str__(self) -> str:
        return "branch %s" % str(self.target)

    def accept(self, v: TACVisitor) -> None:
        v.visitBranch(self)


# Branching with conditions.
class CondBranch(TACInstr):
    def __init__(self, op: CondBranchOp, cond: Temp, target: Label) -> None:
        super().__init__(InstrKind.COND_JMP, [], [cond], target)
        self.op = op
        self.cond = cond
        self.target = target

    def __str__(self) -> str:
        return "if (%s %s) branch %s" % (
            self.cond,
            "== 0" if self.op == CondBranchOp.BEQ else "!= 0",
            str(self.target),
        )

    def accept(self, v: TACVisitor) -> None:
        v.visitCondBranch(self)


# Return instruction.
class Return(TACInstr):
    def __init__(self, value: Optional[Temp]) -> None:
        if value is None:
            super().__init__(InstrKind.RET, [], [], None)
        else:
            super().__init__(InstrKind.RET, [], [value], None)
        self.value = value

    def __str__(self) -> str:
        return "return" if (self.value is None) else ("return " + str(self.value))

    def accept(self, v: TACVisitor) -> None:
        v.visitReturn(self)


# Annotation (used for debugging).
class Memo(TACInstr):
    def __init__(self, msg: str) -> None:
        super().__init__(InstrKind.SEQ, [], [], None)
        self.msg = msg

    def __str__(self) -> str:
        return "memo '%s'" % self.msg

    def accept(self, v: TACVisitor) -> None:
        v.visitMemo(self)


# Label (function entry or branching target).
class Mark(TACInstr):
    def __init__(self, label: Label) -> None:
        super().__init__(InstrKind.LABEL, [], [], label)

    def __str__(self) -> str:
        return "%s:" % str(self.label)

    def accept(self, v: TACVisitor) -> None:
        v.visitMark(self)


# setup para for func when call the func
class SetupPara(TACInstr):
    def __init__(self, src: Temp, index: int) -> None:
        super().__init__(InstrKind.SEQ, [], [src], None)
        self.src = src
        self.index = index

    def __str__(self) -> str:
        return "setup para %s , index is %d" % (self.src, self.index)

    def accept(self, v: TACVisitor) -> None:
        v.visitSetupPara(self)


# call the func
class Call(TACInstr):
    def __init__(self, target: Label, dst: Temp, para_cnt: int) -> None:
        super().__init__(InstrKind.SEQ, [dst], [], target)
        self.dst = dst
        self.target = target
        self.para_cnt = para_cnt

    def __str__(self) -> str:
        return "call func dst is %s ,target is %s" % (self.dst, str(self.target))

    def accept(self, v: TACVisitor) -> None:
        v.visitCall(self)


class Alloc(TACInstr):
    def __init__(self, dst: Temp, size: int) -> None:
        super().__init__(InstrKind.SEQ, [dst], [], None)
        self.dst = dst
        self.size = size

    def __str__(self) -> str:
        return "%s <- alloc %d" % (str(self.dst), self.size)

    def accept(self, v: TACVisitor) -> None:
        v.visitAlloc(self)


class LoadAddress(TACInstr):
    def __init__(self, name: str, dst: Temp) -> None:
        super().__init__(InstrKind.SEQ, [dst], [], None)
        self.dst = dst
        self.name = name

    def __str__(self) -> str:
        return "load address of %s to %s" % (self.name, str(self.dsts[0]))

    def accept(self, v: TACVisitor) -> None:
        v.visitLoadAddress(self)


class Load(TACInstr):
    def __init__(self, dst: Temp, base: Temp, offset: int) -> None:
        super().__init__(InstrKind.SEQ, [dst], [base], None)
        self.dst = dst
        self.base = base
        self.offset = offset

    def __str__(self) -> str:
        return "%s <- load %d(%s)" % (str(self.dsts[0]), self.offset, str(self.srcs[0]))

    def accept(self, v: TACVisitor) -> None:
        v.visitLoad(self)


class Store(TACInstr):
    def __init__(self, src: Temp, base: Temp, offset: int) -> None:
        super().__init__(InstrKind.SEQ, [], [src, base], None)
        self.src = src
        self.base = base
        self.offset = offset

    def __str__(self) -> str:
        return "store %s -> %d(%s)" % (str(self.srcs[0]), self.offset, str(self.srcs[1]))

    def accept(self, v: TACVisitor) -> None:
        v.visitStore(self)
