# Temporary variables.

class Temp:

    def __init__(self, index: int) -> None:
        self.index = index
        self.para_id = -1

    def __str__(self) -> str:
        return "_T" + str(self.index)
