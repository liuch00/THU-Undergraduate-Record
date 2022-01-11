"""
Module that defines a lexer using `ply.lex`.
It won't make your experiment harder if you don't read it.
"""

from functools import wraps
from typing import List

import ply.lex as lex

from frontend.ast import tree
from utils.error import DecafLexError
from .lex import *

error_stack: List[DecafLexError] = []

states = (("multiline", "exclusive"),)


@lex.TOKEN(r"/\*")
def t_multiline(t):
    t.lexer.begin("multiline")


@lex.TOKEN(r"\*/")
def t_multiline_end(t):
    t.lexer.begin("INITIAL")


t_multiline_ignore_all = rf".+?(?=\*/|{t_ignore_Newline})"


@lex.TOKEN(t_ignore_Newline)
def t_ANY_Newline(t):
    t.lexer.lineno += 1


def t_ANY_error(t):
    error_stack.append(DecafLexError(t))
    t.lexer.skip(1)


def _identifier_into_node(f):
    @wraps(f)
    def wrapped(t):
        t = f(t)
        if t.type == "Identifier":
            t.value = tree.Identifier(t.value)
        return t

    return wrapped


t_Identifier = _identifier_into_node(t_Identifier)


def _intlit_into_node(f):
    @wraps(f)
    def wrapped(t):
        t = f(t)
        t.value = tree.IntLiteral(t.value)
        return t

    return wrapped


t_Integer = _intlit_into_node(t_Integer)

lexer = lex.lex()
lexer.error_stack = error_stack  # type: ignore
