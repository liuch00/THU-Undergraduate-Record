from abc import ABC, abstractmethod

from utils.asmcodeprinter import AsmCodePrinter
from utils.tac.reg import Reg
from utils.tac.tacfunc import TACFunc
from .subroutineinfo import SubroutineInfo

"""
AsmEmitter: emit asm code

        printer: use it to output the asm code
allocatableRegs: all the regs that can used in reg alloc
 callerSaveRegs: all the caller save regs that used in reg alloc

        selectInstr: select asm Instr according to the TAC
     emitSubroutine: return a new asmEmitter that used for emitting the asm code for a new fuction
"""


class AsmEmitter(ABC):
    def __init__(self, allocatableRegs: list[Reg], callerSaveRegs: list[Reg]) -> None:
        self.allocatableRegs = allocatableRegs
        self.callerSaveRegs = callerSaveRegs
        self.printer = AsmCodePrinter()

    @abstractmethod
    def selectInstr(self, func: TACFunc) -> tuple[list[str], SubroutineInfo]:
        raise NotImplementedError

    @abstractmethod
    def emitSubroutine(self, info: SubroutineInfo):
        raise NotImplementedError

    @abstractmethod
    def emitEnd(self):
        raise NotImplementedError
