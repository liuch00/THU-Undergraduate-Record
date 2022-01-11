from typing import Final

from utils.label.label import Label, LabelKind
from utils.tac.nativeinstr import NativeInstr
from utils.tac.reg import Reg
from utils.tac.tacinstr import TACInstr
from utils.tac.tacop import BinaryOp, InstrKind, UnaryOp
from utils.tac.tacop import CondBranchOp
from utils.tac.temp import Temp

WORD_SIZE: Final[int] = 4  # in bytes
MAX_INT: Final[int] = 0x7FFF_FFFF


class Riscv:
    ZERO = Reg(0, "x0")  # always zero
    RA = Reg(1, "ra")  # return address
    SP = Reg(2, "sp")  # stack pointer
    GP = Reg(3, "gp")  # global pointer
    TP = Reg(4, "tp")  # thread pointer
    T0 = Reg(5, "t0")
    T1 = Reg(6, "t1")
    T2 = Reg(7, "t2")
    FP = Reg(8, "fp")  # frame pointer
    S1 = Reg(9, "s1")
    A0 = Reg(10, "a0")
    A1 = Reg(11, "a1")
    A2 = Reg(12, "a2")
    A3 = Reg(13, "a3")
    A4 = Reg(14, "a4")
    A5 = Reg(15, "a5")
    A6 = Reg(16, "a6")
    A7 = Reg(17, "a7")
    S2 = Reg(18, "s2")
    S3 = Reg(19, "s3")
    S4 = Reg(20, "s4")
    S5 = Reg(21, "s5")
    S6 = Reg(22, "s6")
    S7 = Reg(23, "s7")
    S8 = Reg(24, "s8")
    S9 = Reg(25, "s9")
    S10 = Reg(26, "s10")
    S11 = Reg(27, "s11")
    T3 = Reg(28, "t3")
    T4 = Reg(29, "t4")
    T5 = Reg(30, "t5")
    T6 = Reg(31, "t6")

    CallerSaved = [T0, T1, T2, T3, T4, T5, T6, A0, A1, A2, A3, A4, A5, A6, A7]

    CalleeSaved = [S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11]

    AllocatableRegs = CallerSaved + CalleeSaved

    ArgRegs = [A0, A1, A2, A3, A4, A5, A6, A7]

    EPILOGUE_SUFFIX = "_exit"

    FMT1 = "{}"
    FMT2 = "{}, {}"
    FMT3 = "{}, {}, {}"
    FMT_OFFSET = "{}, {}({})"

    # Todo FMT4

    class JumpToEpilogue(TACInstr):
        def __init__(self, label: Label) -> None:
            super().__init__(
                InstrKind.RET,
                [],
                [],
                Label(LabelKind.TEMP, label.name + Riscv.EPILOGUE_SUFFIX),
            )

        def __str__(self) -> str:
            return "j " + str(self.label)

    class RiscvLabel(TACInstr):
        def __init__(self, label: Label) -> None:
            super().__init__(InstrKind.LABEL, [], [], label)

        def __str__(self) -> str:
            return str(self.label) + ":"

        def isLabel(self) -> bool:
            return True

    class LoadImm(TACInstr):
        def __init__(self, dst: Temp, value: int) -> None:
            super().__init__(InstrKind.SEQ, [dst], [], None)
            self.value = value

        def __str__(self) -> str:
            return "li " + Riscv.FMT2.format(str(self.dsts[0]), self.value)

    class Move(TACInstr):
        def __init__(self, dst: Temp, src: Temp) -> None:
            super().__init__(InstrKind.SEQ, [dst], [src], None)

        def __str__(self) -> str:
            return "mv " + Riscv.FMT2.format(str(self.dsts[0]), str(self.srcs[0]))

    class Unary(TACInstr):
        def __init__(self, op: UnaryOp, dst: Temp, src: Temp) -> None:
            super().__init__(InstrKind.SEQ, [dst], [src], None)
            self.op = op.__str__()[8:].lower()

        def __str__(self) -> str:
            return "{} ".format(self.op) + Riscv.FMT2.format(
                str(self.dsts[0]), str(self.srcs[0])
            )

    class Binary(TACInstr):
        def __init__(self, op: BinaryOp, dst: Temp, src0: Temp, src1: Temp) -> None:
            super().__init__(InstrKind.SEQ, [dst], [src0, src1], None)
            self.op = op.__str__()[9:].lower()

        def __str__(self) -> str:
            return "{} ".format(self.op) + Riscv.FMT3.format(
                str(self.dsts[0]), str(self.srcs[0]), str(self.srcs[1])
            )

    # edit Branch in step-8
    class Branch(TACInstr):
        def __init__(self, op: str, cond: Temp, target: Label) -> None:
            super().__init__(InstrKind.COND_JMP, [], [cond], target)
            if op == CondBranchOp.BEQ:
                self.op = 'beq'
            else:
                self.op = 'bne'
            self.target = target

        def __str__(self) -> str:
            return self.op + " " + Riscv.FMT3.format(str(Riscv.ZERO), str(self.srcs[0]), str(self.target))

    class Jump(TACInstr):
        def __init__(self, target: Label) -> None:
            super().__init__(InstrKind.JMP, [], [], target)
            self.target = target

        def __str__(self) -> str:
            return "j " + str(self.target)

    class Alloc(TACInstr):
        def __init__(self, dst: Temp, size: int) -> None:
            super().__init__(InstrKind.SEQ, [dst], [], None)
            self.size = size
            self.offset = 0

        def __str__(self) -> str:
            return f"addi {self.dsts[0]}, fp, {self.offset}"

    class LoadWord(TACInstr):
        def __init__(self, dst: Temp, base: Temp, offset: int) -> None:
            super().__init__(InstrKind.SEQ, [dst], [base], None)
            self.offset = offset

        def __str__(self) -> str:
            return f"lw {self.dsts[0]}, {self.offset}({self.srcs[0]})"

    class StoreWord(TACInstr):
        def __init__(self, src: Temp, base: Temp, offset: int) -> None:
            super().__init__(InstrKind.SEQ, [], [src, base], None)
            self.offset = offset

        def __str__(self) -> str:
            return f"sw {self.srcs[0]}, {self.offset}({self.srcs[1]})"

    class CallInstr(TACInstr):
        def __init__(self, func_name: Label, para_cnt: int) -> None:
            super().__init__(InstrKind.SEQ, [], [], func_name)
            self.para_cnt = para_cnt

        def __str__(self) -> str:
            return f"call {self.label.name}"

    class MvInstr(TACInstr):
        def __init__(self, dest: Temp, src: Temp) -> None:
            super().__init__(InstrKind.SEQ, [dest], [src], None)

        def __str__(self) -> str:
            return f"mv {self.dsts[0]}, {self.srcs[0]}"

    class LoadAddressInstr(TACInstr):
        def __init__(self, dest: Temp, name: str) -> None:
            super().__init__(InstrKind.SEQ, [dest], [], None)
            self.name = name

        def __str__(self) -> str:
            return f"la {self.dsts[0]}, {self.name}"

    class SPAdd(NativeInstr):
        def __init__(self, offset: int) -> None:
            super().__init__(InstrKind.SEQ, [Riscv.SP], [Riscv.SP], None)
            self.offset = offset

        def __str__(self) -> str:
            assert -2048 <= self.offset <= 2047  # Riscv imm [11:0]
            return "addi " + Riscv.FMT3.format(
                str(Riscv.SP), str(Riscv.SP), str(self.offset)
            )

    class MoveFP(NativeInstr):
        def __init__(self) -> None:
            super().__init__(InstrKind.SEQ, [Riscv.FP], [Riscv.SP], None)

        def __str__(self) -> str:
            return "mv fp, sp"

    class NativeStoreWord(NativeInstr):
        def __init__(self, src: Reg, base: Reg, offset: int) -> None:
            super().__init__(InstrKind.SEQ, [], [src, base], None)
            self.offset = offset

        def __str__(self) -> str:
            assert -2048 <= self.offset <= 2047  # Riscv imm [11:0]
            return "sw " + Riscv.FMT_OFFSET.format(
                str(self.srcs[0]), str(self.offset), str(self.srcs[1])
            )

    class NativeLoadWord(NativeInstr):
        def __init__(self, dst: Reg, base: Reg, offset: int) -> None:
            super().__init__(InstrKind.SEQ, [dst], [base], None)
            self.offset = offset

        def __str__(self) -> str:
            assert -2048 <= self.offset <= 2047  # Riscv imm [11:0]
            return "lw " + Riscv.FMT_OFFSET.format(
                str(self.dsts[0]), str(self.offset), str(self.srcs[0])
            )

    class NativeReturn(NativeInstr):
        def __init__(self) -> None:
            super().__init__(InstrKind.RET, [Riscv.RA], [], None)

        def __str__(self) -> str:
            return "ret"
