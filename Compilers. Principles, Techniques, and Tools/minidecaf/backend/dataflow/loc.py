from utils.tac.tacinstr import TACInstr

"""
Loc: line of code
"""


class Loc:
    def __init__(self, instr: TACInstr) -> None:
        self.instr = instr
        self.liveIn: set[int] = set()
        self.liveOut: set[int] = set()
