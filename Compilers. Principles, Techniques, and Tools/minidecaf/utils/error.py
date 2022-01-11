from typing import Optional, Union

from utils import find_column


class DecafLexError(Exception):
    def __init__(self, t) -> None:
        super().__init__(
            f"Lex error: invalid token at line {t.lineno}, column {find_column(t.lexer.lexdata, t.lexpos)}"
        )
        self.token = t


class DecafSyntaxError(Exception):
    def __init__(self, t, extra: Optional[str] = None) -> None:
        if t is not None:
            msg = (
                    f"Syntax error: line {t.lineno}, column {find_column(t.lexer.lexdata, t.lexpos)}"
                    + (extra or "")
            )
        else:
            msg = f"Syntax error: " + (extra or "")
        super().__init__(msg)
        self.token = t


class DecafNoMainFuncError(Exception):
    def __init__(self) -> None:
        super().__init__("Semantic error: can not find 'main' function")


class DecafDeclConflictError(Exception):
    def __init__(self, name: str) -> None:
        super().__init__("Semantic error: declaration conflict '%s'" % name)


class DecafBadIntValueError(Exception):
    def __init__(self, val: Union[str, int]) -> None:
        super().__init__("Semantic error: bad integer value " + str(val))


class DecafUndefinedVarError(Exception):
    def __init__(self, name: str) -> None:
        super().__init__("Semantic error: undefined variable '%s'" % name)


class DecafUndefinedFuncError(Exception):
    def __init__(self, name: str) -> None:
        super().__init__("Semantic error: undefined function '%s'" % name)


class DecafBreakOutsideLoopError(Exception):
    def __init__(self) -> None:
        super().__init__("Semantic error: 'break' outside any loops")


class DecafContinueOutsideLoopError(Exception):
    def __init__(self) -> None:
        super().__init__("Semantic error: 'continue' outside any loops")


class DecafGlobalVarDefinedTwiceError(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(
            "Semantic error: global variable '%s' has been defined twice" % name
        )


class DecafGlobalVarBadInitValueError(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(
            "Semantic error: the initial value of global variable '%s' must be an integer constant"
            % name
        )


class DecafBadArraySizeError(Exception):
    def __init__(self) -> None:
        super().__init__("Semantic error: the array size must be positive integer")


class DecafBadIndexError(Exception):
    def __init__(self, name: Optional[str] = None) -> None:
        if name:
            super().__init__("Semantic error: bad index on '%s'" % name)
        else:
            super().__init__("Semantic error: bad index")


class DecafTypeMismatchError(Exception):
    def __init__(self) -> None:
        super().__init__("Semantic error: type mismatch")


class DecafBadReturnTypeError(Exception):
    def __init__(self) -> None:
        super().__init__("Semantic error: bad return type")


class DecafBadFuncCallError(Exception):
    def __init__(self, name: str) -> None:
        super().__init__("Semantic error: bad function call '%s'" % name)


class DecafParameterMisMatchError(Exception):
    def __init__(self, name: str, expect: int, actual: int) -> None:
        super().__init__("Semantic error: expect %d parameters for function call '%s', got %d" % (expect, name, actual))


class DecafBadAssignTypeError(Exception):
    def __init__(self) -> None:
        super().__init__("Semantic error: cannot assign to an array")


class IllegalArgumentException(Exception):
    def __init__(self) -> None:
        super().__init__("error: encounter a non-returned basic block")


class NullPointerException(Exception):
    def __init__(self) -> None:
        super().__init__("NullPointerException")
