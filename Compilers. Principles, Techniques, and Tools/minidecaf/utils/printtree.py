from frontend.ast.node import Node


class TreePrinter:
    l = "["
    r = "]"
    lr = l + r

    def __init__(self, indentLen=4) -> None:
        self.indentLen = indentLen
        self.indentNum = 0

    def work(self, element) -> None:
        if element is None:
            self.printLine("<None: here is a bug>")

        elif isinstance(element, Node):
            if element.is_leaf():
                self.printLine(str(element))
                return

            if len(element) == 0:
                self.printLine(f"{element.name} {self.lr}")
                return

            self.printLine(f"{element.name} {self.l}")
            self.incIndent()
            for it in element:
                self.work(it)
            self.decIndent()
            self.printLine(self.r)

        elif isinstance(element, list):
            self.printLine("List")
            self.incIndent()
            if len(element) == 0:
                self.printLine("<empty>")
            else:
                for it in element:
                    self.work(it)
            self.decIndent()

        else:
            self.printLine(str(element))

    def outputIndent(self) -> None:
        if self.indentNum > 0:
            print(" " * self.indentLen * self.indentNum, end="")

    def printLine(self, s: str) -> None:
        self.outputIndent()
        print(s)

    def incIndent(self) -> None:
        self.indentNum += 1

    def decIndent(self) -> None:
        self.indentNum -= 1
