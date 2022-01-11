from abc import ABC, abstractmethod

from backend.subroutineinfo import SubroutineInfo
from utils.label.label import Label
from utils.tac.nativeinstr import NativeInstr
from utils.tac.reg import Reg, Temp
from .asmemitter import AsmEmitter

"""
SubroutineEmitter: emit asm code for a fuction

printer: the same as AsmEmitter, which we use to output the asm code
   info: subroutineInfo for the function

emitEnd: output all the asm code for the function
"""


class SubroutineEmitter(ABC):
    def __init__(self, emitter: AsmEmitter, info: SubroutineInfo) -> None:
        self.info = info
        self.printer = emitter.printer

    @abstractmethod
    def emitComment(self, comment: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def emitAlloc(self, size: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def emitStoreToStack(self, src: Reg) -> None:
        raise NotImplementedError

    @abstractmethod
    def emitLoadFromStack(self, dst: Reg, src: Temp):
        raise NotImplementedError

    @abstractmethod
    def emitNative(self, instr: NativeInstr):
        raise NotImplementedError

    @abstractmethod
    def emitLabel(self, label: Label):
        raise NotImplementedError

    @abstractmethod
    def emitEnd(self):
        raise NotImplementedError
