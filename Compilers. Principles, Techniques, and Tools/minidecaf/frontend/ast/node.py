"""
Module that contains enums which list out all operators,
base class `Node` of all AST nodes,
and a helper type `NullType` along with its instance `NULL`.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, unique
from typing import Any, Optional, TypeVar

from .visitor import Visitor

_T = TypeVar("_T", bound=Enum)

T = TypeVar("T")
U = TypeVar("U", covariant=True)


class Operator(Enum):
    """
    Base class of operators.
    """

    @classmethod
    def backward_search(cls: type[_T], s: str) -> _T:
        """
        A helper function to find the corresponding enumeration entry by its value.
        """
        try:
            d = cls.__dict__["_backward"]
        except KeyError:
            cls._backward = {item.value: item for item in cls}  # type: ignore
            d = cls._backward  # type: ignore
        return d[s]  # type: ignore


@unique
class UnaryOp(Operator):
    """
    Enumerates all unary operators
    """

    Neg = "-"
    BitNot = "~"
    LogicNot = "!"


@unique
class BinaryOp(Operator):
    """
    Enumerates all binary operators
    """

    Assign = "="

    LogicOr = "||"

    LogicAnd = "&&"

    BitOr = "|"

    Xor = "^"

    BitAnd = "&"

    EQ = "=="
    NE = "!="

    LT = "<"
    GT = ">"
    LE = "<="
    GE = ">="

    Add = "+"
    Sub = "-"

    Mul = "*"
    Div = "/"
    Mod = "%"


"""
Since there's only one single ternary operator `?:`,
it's no need to make a enumeration for it.
"""


class Node(ABC):
    """
    Base class of all AST nodes.
    """

    def __init__(self, name: str) -> None:
        """Constructor.
        `name`: name of this kind of node. Used when represents the node by a string.
        `_attrs`: used to store additional information on AST nodes.
        """
        self.name = name
        self._attrs = dict[str, Any]()

    @abstractmethod
    def __len__(self) -> int:
        """Returns its children count."""
        raise NotImplementedError

    @abstractmethod
    def __getitem__(self, key: int) -> Node:
        """
        Get one of its children by index.
        Not that children of a AST node are always AST nodes.
        """
        raise NotImplementedError

    @abstractmethod
    def accept(self, v: Visitor[T, U], ctx: T) -> Optional[U]:
        """Dispatcher method used along with a `Visitor`."""
        raise NotImplementedError

    def is_leaf(self):
        return False

    def setattr(self, name: str, value: Any):
        """Set additional information on AST node."""
        self._attrs[name] = value

    def getattr(self, name: str) -> Any:
        """
        Get additional information on AST node.
        Note that the default return value is `None` when the given name is not present.
        """
        return self._attrs.get(name, None)

    def __iter__(self):
        """Iterates its children."""
        for i in range(0, len(self)):
            yield self[i]

    def __bool__(self):
        """
        Used in contexts like `if`.
        Makes null-checking easier.
        """
        return True

    def __str__(self) -> str:
        """
        Recursively stringify itself and its children.
        Override this method when necesssary.
        """
        if len(self) == 0:
            return self.name

        return "{}[{}]".format(
            self.name,
            ", ".join(map(str, self)),
        )

    def __repr__(self) -> str:
        return self.__str__()


class NullType(Node):
    """
    Helper class that represents an empty node.
    You can take `If` in `.tree` as an example.
    """

    def __init__(self) -> None:
        super().__init__("NULL")

    def __getitem__(self, key: int) -> Node:
        return super().__getitem__(key)

    def __len__(self) -> int:
        return 0

    def __bool__(self):
        return False

    def accept(self, v: Visitor[T, U], ctx: T) -> Optional[U]:
        return v.visitNULL(self, ctx)

    def is_leaf(self):
        return True


"This should be the only instance of NullType."
NULL = NullType()
