from enum import Enum, auto, unique


@unique
class LabelKind(Enum):
    TEMP = auto()
    FUNC = auto()
    BLOCK = auto()


class Label:
    def __init__(self, kind: LabelKind, name: str) -> None:
        self.kind = kind
        self.name = name

    def __str__(self) -> str:
        return self.name

    def isFunc(self) -> bool:
        return self.kind == LabelKind.FUNC
