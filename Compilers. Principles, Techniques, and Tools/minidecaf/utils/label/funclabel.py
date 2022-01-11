from .label import Label, LabelKind


class FuncLabel(Label):
    def __init__(self, name: str) -> None:
        super().__init__(LabelKind.FUNC, name)
        self.func = name

    def __str__(self) -> str:
        return "FUNCTION<%s>" % self.func


MAIN_LABEL = FuncLabel("main")
