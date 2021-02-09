from typing import Union

from ..types import TealType
from ..ir import TealOp, Op, TealBlock
from ..errors import TealInputError
from .leafexpr import LeafExpr

class Int(LeafExpr):
    """An expression that represents a uint64."""

    def __init__(self, value: int) -> None:
        """Create a new uint64.

        Args:
            value: The integer value this uint64 will represent. Must be a positive value less than
                2**64.
        """
        if type(value) is not int:
            raise TealInputError("invalid input type {} to Int".format(type(value))) 
        elif value >= 0 and value < 2 ** 64:
            self.value = value
        else:
            raise TealInputError("Int {} is out of range".format(value))

    def __teal__(self):
        op = TealOp(Op.int, self.value)
        return TealBlock.FromOp(op)

    def __str__(self):
        return "(Int: {})".format(self.value)

    def type_of(self):
        return TealType.uint64

Int.__module__ = "pyteal"

intEnumValues = {
    # OnComplete values
    "NoOp": 0,
    "OptIn": 1,
    "CloseOut": 2,
    "ClearState": 3,
    "UpdateApplication": 4,
    "DeleteApplication": 5,
    # TxnType values
    "unknown": 0,
    "pay": 1,
    "keyreg": 2,
    "acfg": 3,
    "axfer": 4,
    "afrz": 5,
    "appl": 6,
}

class EnumInt(LeafExpr):
    """An expression that represents uint64 enum values."""

    def __init__(self, name: str) -> None:
        """Create an expression to reference a uint64 enum value.
        
        Args:
            name: The name of the enum value.
        """
        if name not in intEnumValues:
            raise TealInputError("Unknown int enum value: {}".format(name))
        self.name = name

    def __teal__(self):
        op = TealOp(Op.int, intEnumValues[self.name])
        return TealBlock.FromOp(op)

    def __str__(self):
        return "(IntEnum: {})".format(self.name)

    def type_of(self):
        return TealType.uint64

EnumInt.__module__ = "pyteal"
