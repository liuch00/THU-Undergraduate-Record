from enum import Enum, auto, unique
from typing import Optional

from backend.dataflow.loc import Loc
from utils.label.label import Label

"""
BlockKind
depend on the last instr of the basicblock
"""


@unique
class BlockKind(Enum):
    CONTINUOUS = auto()
    END_BY_JUMP = auto()
    END_BY_COND_JUMP = auto()
    END_BY_RETURN = auto()


"""
BasicBlock
Sequence of instrs executed sequentially (from baidu)

 kind: BlockKind
   id: the id of the block
label: the label of the block, which will be used in CfgBuilder
 locs: sequence of instrs

 define: the temps definded in this basicblock
liveUse: the temps used in this basicblock before it's redefine
 liveIn: the active temps in the start of the basicblock
liveOut: the active temps in the end of the basicblock
"""


class BasicBlock:
    def __init__(
            self, kind: BlockKind, id: int, label: Optional[Label], locs: list[Loc]
    ) -> None:
        self.kind = kind
        self.id = id
        self.label = label
        self.locs: list[Loc] = locs.copy()

        self.define: set[int] = set()
        self.liveUse: set[int] = set()
        self.liveIn: set[int] = set()
        self.liveOut: set[int] = set()

    def isEmpty(self):
        return len(self.locs) == 0

    def iterator(self):
        return iter(self.locs)

    def backwardIterator(self):
        return reversed(self.locs)

    def allSeq(self):
        if self.kind is BlockKind.CONTINUOUS:
            return self.locs
        return self.locs[0:-1]

    def getLastInstr(self):
        return self.locs[-1].instr
