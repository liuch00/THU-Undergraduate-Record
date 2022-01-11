import inspect
import types
from typing import Optional, TypeVar


def caller_module():
    frame = inspect.stack()[2]
    module = inspect.getmodule(frame[0])
    for frame in inspect.stack():
        print(frame)
    return module


def imports():
    mod = caller_module()
    return {
        val.__name__
        for val in mod.__dict__.values()
        if isinstance(val, types.ModuleType)
    }


def try_else(job, onSucceed, onFail):
    try:
        ret = job()
    except BaseException as e:
        return onFail(e)
    else:
        return onSucceed(ret)


def find_column(_input: str, lexpos: int):
    line_start = _input.rfind("\n", 0, lexpos)
    return lexpos - line_start


def get_line(_input: str, lineno: int):
    lines = get_line.__dict__.setdefault(_input, _input.splitlines())
    return lines[lineno - 1]


def get_grammar(path: Optional[str] = None):
    import re

    from frontend.lexer import lex

    lexes = tuple(
        (val, name.removeprefix("t_"))
        for name, val in lex.__dict__.items()
        if (
                isinstance(val, str)
                and not name.startswith("_")
                and not name.startswith("t_ignore_")
        )
    ) + tuple(lex.reserved.items())
    lexes = map(
        lambda t: (re.compile(f"'{t[0]}'"), t[1]),
        lexes,
    )

    with open(path if path else "grammar", "r") as f:
        grammar = f.read()

    for reg, tokname in lexes:
        grammar = reg.sub(tokname, grammar)
    return grammar


T = TypeVar("T")
U = TypeVar("U")
