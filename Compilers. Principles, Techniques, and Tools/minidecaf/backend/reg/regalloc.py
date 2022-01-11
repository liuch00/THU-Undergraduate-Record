from abc import ABC, abstractmethod

from backend.dataflow.cfg import CFG
from backend.riscv.riscvasmemitter import RiscvAsmEmitter
from backend.subroutineinfo import SubroutineInfo

"""
RegAlloc: a abstract class for reg alloc
"""


class RegAlloc(ABC):
    def __init__(self, emitter: RiscvAsmEmitter) -> None:
        self.emitter = emitter

    @abstractmethod
    def accept(self, graph: CFG, info: SubroutineInfo) -> None:
        raise NotImplementedError
