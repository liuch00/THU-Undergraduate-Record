from .label import Label, LabelKind


class BlockLabel(Label):
    def __init__(self, name: str) -> None:
        super().__init__(LabelKind.BLOCK, "_L" + name)
