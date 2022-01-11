from typing import Optional

from utils.label.label import Label
from utils.tac.reg import Reg
from .tacop import InstrKind


class NativeInstr:
    def __init__(
            self,
            kind: InstrKind,
            dsts: list[Reg],
            srcs: list[Reg],
            label: Optional[Label],
            instrString: Optional[str] = None,
    ) -> None:
        self.kind = kind
        self.dsts = dsts
        self.srcs = srcs
        self.label = label
        self.instrString = instrString

    def __str__(self) -> str:
        assert self.instrString is not None
        return self.instrString

    def nativeComment(comment: str):
        return NativeInstr(InstrKind.SEQ, [], [], None, comment)

    def getRead(self) -> list[Reg]:
        return self.srcs

    def getWritten(self) -> list[Reg]:
        return self.dsts

    def isLabel(self) -> bool:
        return self.kind == InstrKind.LABEL

    def isSequential(self) -> bool:
        return self.kind == InstrKind.SEQ

    def isReturn(self) -> bool:
        return self.kind == InstrKind.RET
