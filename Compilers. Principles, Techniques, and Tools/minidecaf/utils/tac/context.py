from __future__ import annotations

from utils.label.blocklabel import BlockLabel
from utils.label.funclabel import FuncLabel


class Context:
    def __init__(self) -> None:
        self.labels = {}
        self.funcs = []
        self.nextTempLabelId = 1

    def putFuncLabel(self, name: str) -> None:
        self.labels[name] = FuncLabel(name)

    def getFuncLabel(self, name: str) -> FuncLabel:
        return self.labels[name]

    def freshLabel(self) -> BlockLabel:
        name = str(self.nextTempLabelId)
        self.nextTempLabelId += 1
        return BlockLabel(name)
