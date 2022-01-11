from __future__ import annotations

from typing import Iterator, Protocol, Union

import frontend.ast.node as node
from utils.error import DecafLexError
from . import lex
# * replace the '.ply-lexer' by '.xxx' to use your own-defined lexer, where 'xxx' is the module/package name of it
# * note that your lexer should be iterable, and should have the method 'input' in order to accept the input source file
from .ply_lexer import lexer as ply_lexer


class LexToken(Protocol):
    def __init__(self) -> None:
        self.type: str
        self.value: Union[str, node.Node]
        self.lineno: int
        self.lexpos: int
        self.lexer: Lexer

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...


class Lexer(Protocol):
    def __init__(self) -> None:
        self.lexdata: str
        self.lexpos: int
        self.lineno: int

        self.error_stack: list[DecafLexError]

    def input(self, s: str) -> None:
        ...

    def token(self) -> LexToken:
        ...

    def __iter__(self) -> Iterator[LexToken]:
        ...

    def __next__(self) -> LexToken:
        ...


lexer: Lexer = ply_lexer

__all__ = [
    "lexer",
    "lex",
    "LexToken",
    "Lexer",
    "ply_lexer",
]
