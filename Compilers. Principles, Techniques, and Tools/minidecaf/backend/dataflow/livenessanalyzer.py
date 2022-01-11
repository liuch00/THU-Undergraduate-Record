from backend.dataflow.basicblock import BasicBlock
from backend.dataflow.cfg import CFG

"""
LivenessAnalyzer: do the liveness analysis according to the CFG
"""


class LivenessAnalyzer:
    def __init__(self) -> None:
        pass

    def accept(self, graph: CFG):
        for bb in graph.nodes:
            self.computeDefAndLiveUseFor(bb)
            bb.liveIn = set()
            bb.liveIn.update(bb.liveUse)
            bb.liveOut = set()

        changed = True
        while changed:
            changed = False
            for bb in graph.nodes:
                for next in graph.getSucc(bb.id):
                    bb.liveOut.update(graph.getBlock(next).liveIn)

                liveOut = bb.liveOut.copy()
                for v in bb.define:
                    liveOut.discard(v)

                before = len(bb.liveIn)
                bb.liveIn.update(liveOut)
                after = len(bb.liveIn)

                if before != after:
                    changed = True

        for bb in graph.nodes:
            self.analyzeLivenessForEachLocIn(bb)

    def computeDefAndLiveUseFor(self, bb: BasicBlock):
        bb.define = set()
        bb.liveUse = set()
        for loc in bb.iterator():
            for read in loc.instr.getRead():
                if not read in bb.define:
                    bb.liveUse.add(read)
            bb.define.update(loc.instr.getWritten())

    def analyzeLivenessForEachLocIn(self, bb: BasicBlock):
        liveOut = bb.liveOut.copy()
        for loc in bb.backwardIterator():
            loc.liveOut = liveOut.copy()

            for v in loc.instr.getWritten():
                liveOut.discard(v)

            liveOut.update(loc.instr.getRead())
            loc.liveIn = liveOut.copy()
