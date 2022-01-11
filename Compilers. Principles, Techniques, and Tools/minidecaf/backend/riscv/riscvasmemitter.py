from backend.asmemitter import AsmEmitter
from utils.error import IllegalArgumentException
from utils.label.label import LabelKind
from utils.riscv import Riscv, WORD_SIZE
from utils.tac.tacfunc import TACFunc
from utils.tac.tacinstr import *
from utils.tac.tacprog import GlobalVarInfo
from utils.tac.tacvisitor import TACVisitor
from ..subroutineemitter import SubroutineEmitter
from ..subroutineinfo import SubroutineInfo

"""
RiscvAsmEmitter: an AsmEmitter for RiscV
"""


class RiscvAsmEmitter(AsmEmitter):
    def __init__(
            self,
            allocatableRegs: list[Reg],
            callerSaveRegs: list[Reg],
            glob_var: list[GlobalVarInfo]
    ) -> None:
        super().__init__(allocatableRegs, callerSaveRegs)

        for glob in glob_var:
            if glob.init is None:
                self.printer.println(".bss")
                self.printer.println(f".globl {glob.name}")
                self.printer.println(f"{glob.name}:")
                self.printer.println(f"    .space {glob.size}")
            else:
                self.printer.println(".data")
                self.printer.println(f".globl {glob.name}")
                self.printer.println(f"{glob.name}:")
                self.printer.println(f"    .word {glob.init}")

        self.printer.println(".text")
        self.printer.println(".global main")
        self.printer.println("")

        self.last_call_para_count = -1

    # transform tac instrs to RiscV instrs
    # collect some info which is saved in SubroutineInfo for SubroutineEmitter
    def selectInstr(self, func: TACFunc) -> tuple[list[str], SubroutineInfo]:

        selector: RiscvAsmEmitter.RiscvInstrSelector = (
            RiscvAsmEmitter.RiscvInstrSelector(func.entry)
        )
        for instr in func.getInstrSeq():
            instr.accept(selector)

        info = SubroutineInfo(func.entry)

        return (selector.seq, info)

    # use info to construct a RiscvSubroutineEmitter
    def emitSubroutine(self, info: SubroutineInfo):
        return RiscvSubroutineEmitter(self, info)

    # return all the string stored in asmcodeprinter
    def emitEnd(self):
        return self.printer.close()

    class RiscvInstrSelector(TACVisitor):
        def __init__(self, entry: Label) -> None:
            self.entry = entry
            self.seq = []

        # in step11, you need to think about how to deal with globalTemp in almost all the visit functions. 
        def visitReturn(self, instr: Return) -> None:
            if instr.value is not None:
                self.seq.append(Riscv.Move(Riscv.A0, instr.value))
            else:
                self.seq.append(Riscv.LoadImm(Riscv.A0, 0))
            self.seq.append(Riscv.JumpToEpilogue(self.entry))

        def visitMark(self, instr: Mark) -> None:
            self.seq.append(Riscv.RiscvLabel(instr.label))

        def visitLoadImm4(self, instr: LoadImm4) -> None:
            self.seq.append(Riscv.LoadImm(instr.dst, instr.value))

        def visitUnary(self, instr: Unary) -> None:
            self.seq.append(Riscv.Unary(instr.op, instr.dst, instr.operand))

        def visitBinary(self, instr: Binary) -> None:
            self.seq.append(Riscv.Binary(instr.op, instr.dst, instr.lhs, instr.rhs))

        def visitCondBranch(self, instr: CondBranch) -> None:
            # add op in step-8
            self.seq.append(Riscv.Branch(instr.op, instr.cond, instr.label))

        def visitBranch(self, instr: Branch) -> None:
            self.seq.append(Riscv.Jump(instr.target))

        def visitAssign(self, instr: Assign) -> None:
            self.seq.append(Riscv.Move(instr.dst, instr.src))

        def visitSetupPara(self, instr: SetupPara) -> None:
            self.seq.append(Riscv.StoreWord(instr.src, Riscv.SP, - instr.index * WORD_SIZE))

        def visitCall(self, instr: Call) -> None:
            self.seq.append(Riscv.CallInstr(instr.target, instr.para_cnt))
            self.seq.append(Riscv.MvInstr(instr.dst, Riscv.A0))

        def visitAlloc(self, instr: Alloc) -> None:
            self.seq.append(Riscv.Alloc(instr.dst, instr.size))

        def visitLoad(self, instr: Load) -> None:
            self.seq.append(Riscv.LoadWord(instr.dst, instr.base, instr.offset))

        def visitStore(self, instr: Store) -> None:
            self.seq.append(Riscv.StoreWord(instr.src, instr.base, instr.offset))

        def visitLoadAddress(self, instr: LoadAddress) -> None:
            self.seq.append(Riscv.LoadAddressInstr(instr.dst, instr.name))

        # in step9, you need to think about how to pass the parameters and how to store and restore callerSave regs
        # in step11, you need to think about how to store the array 


"""
RiscvAsmEmitter: an SubroutineEmitter for RiscV
"""


class RiscvSubroutineEmitter(SubroutineEmitter):
    def __init__(self, emitter: RiscvAsmEmitter, info: SubroutineInfo) -> None:
        super().__init__(emitter, info)

        self.nextLocalOffset = -8

        # the buf which stored all the NativeInstrs in this function
        self.buf: list[NativeInstr] = []

        # from temp to int
        # record where a temp is stored in the stack
        self.offsets = {}

        self.printer.printLabel(info.funcLabel)

        # in step9, step11 you can compute the offset of local array and parameters here

    def emitComment(self, comment: str) -> None:
        # you can add some log here to help you debug
        pass

    def emitAlloc(self, size: int) -> int:
        self.nextLocalOffset -= size
        return self.nextLocalOffset

    # store some temp to stack
    # usually happen when reaching the end of a basicblock
    # in step9, you need to think about the fuction parameters here
    def emitStoreToStack(self, src: Reg) -> None:
        if src.temp.index not in self.offsets:
            self.nextLocalOffset -= 4
            self.offsets[src.temp.index] = self.nextLocalOffset
        self.buf.append(
            Riscv.NativeStoreWord(src, Riscv.FP, self.offsets[src.temp.index])
        )

    # load some temp from stack
    # usually happen when using a temp which is stored to stack before
    # in step9, you need to think about the fuction parameters here
    def emitLoadFromStack(self, dst: Reg, src: Temp):
        if src.para_id >= 0:
            self.buf.append(Riscv.NativeLoadWord(dst, Riscv.FP, src.para_id * WORD_SIZE))
        elif src.index not in self.offsets:
            raise IllegalArgumentException()
        else:
            self.buf.append(Riscv.NativeLoadWord(dst, Riscv.FP, self.offsets[src.index]))

    # add a NativeInstr to buf
    # when calling the fuction emitEnd, all the instr in buf will be transformed to RiscV code
    def emitNative(self, instr: NativeInstr):
        self.buf.append(instr)

    def emitLabel(self, label: Label):
        self.buf.append(Riscv.RiscvLabel(label).toNative([], []))

    def emitEnd(self):
        self.printer.printComment("start of prologue")
        self.printer.printInstr(Riscv.NativeStoreWord(Riscv.RA, Riscv.SP, -4))
        self.printer.printInstr(Riscv.NativeStoreWord(Riscv.FP, Riscv.SP, -8))
        self.printer.printInstr(Riscv.MoveFP())
        self.printer.printInstr(Riscv.SPAdd(self.nextLocalOffset))

        self.printer.printComment("end of prologue")
        self.printer.println("")

        self.printer.printComment("start of body")

        # using asmcodeprinter to output the RiscV code
        for instr in self.buf:
            self.printer.printInstr(instr)

        self.printer.printComment("end of body")
        self.printer.println("")

        self.printer.printLabel(
            Label(LabelKind.TEMP, self.info.funcLabel.name + Riscv.EPILOGUE_SUFFIX)
        )
        self.printer.printComment("start of epilogue")

        self.printer.printInstr(Riscv.SPAdd(-self.nextLocalOffset))
        self.printer.printInstr(Riscv.NativeLoadWord(Riscv.RA, Riscv.SP, -4))
        self.printer.printInstr(Riscv.NativeLoadWord(Riscv.FP, Riscv.SP, -8))

        self.printer.printComment("end of epilogue")
        self.printer.println("")

        self.printer.printInstr(Riscv.NativeReturn())
        self.printer.println("")
