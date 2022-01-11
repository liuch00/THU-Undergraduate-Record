from typing import Optional, Protocol, cast

from frontend.ast.tree import Program
from frontend.lexer import Lexer
from utils.error import DecafSyntaxError
from .ply_parser import parser as _parser


class Parser(Protocol):
    def __init__(self) -> None:
        self.error_stack: list[DecafSyntaxError]

    def parse(self, input: str, lexer: Optional[Lexer] = None) -> Program:
        ...


parser = cast(Parser, _parser)

__all__ = [
    "parser",
]
