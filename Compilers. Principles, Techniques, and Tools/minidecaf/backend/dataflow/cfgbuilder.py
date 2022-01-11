from backend.dataflow.basicblock import BasicBlock, BlockKind
from backend.dataflow.loc import Loc
from utils.error import IllegalArgumentException, NullPointerException
from utils.tac.tacinstr import InstrKind, TACInstr

from .cfg import CFG

"""
CFGBuilder: from the sequence of instrs to build a control flow graph
"""


class CFGBuilder:
    def __init__(self) -> None:
        self.bbs: list[BasicBlock] = []
        self.buf: list[Loc] = []
        self.currentBBLabel = None
        self.labelsToBBs = {}

    def buildFrom(self, seq: list[TACInstr]):
        for item in seq:
            if item.isLabel():
                if item.label.isFunc():
                    pass
                else:
                    self.close()
                    self.currentBBLabel = item.label
            else:
                self.buf.append(Loc(item))
                if not item.isSequential():
                    if item.kind is InstrKind.JMP:
                        kind = BlockKind.END_BY_JUMP
                    elif item.kind is InstrKind.COND_JMP:
                        kind = BlockKind.END_BY_COND_JUMP
                    elif item.kind is InstrKind.RET:
                        kind = BlockKind.END_BY_RETURN
                    else:
                        kind = None
                    bb = BasicBlock(kind, len(self.bbs), self.currentBBLabel, self.buf)
                    self.save(bb)

        if not len(self.buf) == 0:
            raise IllegalArgumentException

        edges = []
        now = 0
        while now < len(self.bbs):
            bb: BasicBlock = self.bbs[now]
            now += 1

            if bb.kind is BlockKind.END_BY_JUMP:
                if self.labelsToBBs.get(bb.getLastInstr().label) is None:
                    raise NullPointerException
                edges.append((bb.id, self.labelsToBBs.get(bb.getLastInstr().label)))
            elif bb.kind is BlockKind.END_BY_COND_JUMP:
                if self.labelsToBBs.get(bb.getLastInstr().label) is None:
                    raise NullPointerException
                edges.append((bb.id, self.labelsToBBs.get(bb.getLastInstr().label)))
                if now < len(self.bbs) - 1:
                    edges.append((bb.id, bb.id + 1))
            elif bb.kind is BlockKind.END_BY_RETURN:
                pass
            else:
                if now < len(self.bbs):
                    edges.append((bb.id, bb.id + 1))

        # 进行bb的可达性检测
        is_reach = {0: False}
        while 1:
            new_list = []
            for edge in edges:
                if edge[0] in is_reach or edge[0] in new_list:
                    if not (edge[1] in is_reach or edge[1] in new_list):
                        new_list.append(edge[1])
            if len(new_list) <= 0:
                break
            for newbb in new_list:
                is_reach[newbb] = False
        for bb in self.bbs:
            bb.reachable = (bb.id in is_reach)

        return CFG(self.bbs, edges)

    def save(self, bb: BasicBlock):
        self.bbs.append(bb)
        self.buf.clear()
        self.currentBBLabel = None

        if bb.label is not None:
            self.labelsToBBs[bb.label] = bb.id

    def close(self):
        bb = BasicBlock(
            BlockKind.CONTINUOUS, len(self.bbs), self.currentBBLabel, self.buf
        )
        self.save(bb)
