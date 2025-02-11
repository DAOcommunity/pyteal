from typing import TYPE_CHECKING
from enum import Enum

from ..types import TealType
from ..errors import verifyFieldVersion
from ..ir import TealOp, Op, TealBlock
from .leafexpr import LeafExpr

if TYPE_CHECKING:
    from ..compiler import CompileOptions

class GlobalField(Enum):
    min_txn_fee = (0, "MinTxnFee", TealType.uint64, 2)
    min_balance = (1, "MinBalance", TealType.uint64, 2)
    max_txn_life = (2, "MaxTxnLife", TealType.uint64, 2)
    zero_address = (3, "ZeroAddress", TealType.bytes, 2)
    group_size = (4, "GroupSize", TealType.uint64, 2)
    logic_sig_version = (5, "LogicSigVersion", TealType.uint64, 2)
    round = (6, "Round", TealType.uint64, 2)
    latest_timestamp = (7, "LatestTimestamp", TealType.uint64, 2)
    current_app_id = (8, "CurrentApplicationID", TealType.uint64, 2)
    creator_address = (9, "CreatorAddress", TealType.bytes, 3)

    def __init__(self, id: int, name: str, type: TealType, min_version: int) -> None:
        self.id = id
        self.arg_name = name
        self.ret_type = type
        self.min_version = min_version
    
    def type_of(self) -> TealType:
        return self.ret_type

GlobalField.__module__ = "pyteal"

class Global(LeafExpr):
    """An expression that accesses a global property."""

    def __init__(self, field: GlobalField) -> None:
        super().__init__()
        self.field = field

    def __teal__(self, options: 'CompileOptions'):
        verifyFieldVersion(self.field.arg_name, self.field.min_version, options.version)

        op = TealOp(self, Op.global_, self.field.arg_name)
        return TealBlock.FromOp(options, op)
         
    def __str__(self):
        return "(Global {})".format(self.field.arg_name)
    
    def type_of(self):
        return self.field.type_of()

    @classmethod
    def min_txn_fee(cls) -> 'Global':
        """Get the minumum transaction fee in micro Algos."""
        return cls(GlobalField.min_txn_fee)

    @classmethod
    def min_balance(cls) -> 'Global':
        """Get the minumum balance in micro Algos."""
        return cls(GlobalField.min_balance)

    @classmethod
    def max_txn_life(cls) -> 'Global':
        """Get the maximum number of rounds a transaction can have."""
        return cls(GlobalField.max_txn_life)

    @classmethod
    def zero_address(cls) -> 'Global':
        """Get the 32 byte zero address."""
        return cls(GlobalField.zero_address)

    @classmethod
    def group_size(cls) -> 'Global':
        """Get the number of transactions in this atomic transaction group.
        
        This will be at least 1.
        """
        return cls(GlobalField.group_size)

    @classmethod
    def logic_sig_version(cls) -> 'Global':
        """Get the maximum supported TEAL version."""
        return cls(GlobalField.logic_sig_version)
    
    @classmethod
    def round(cls) -> 'Global':
        """Get the current round number."""
        return cls(GlobalField.round)
    
    @classmethod
    def latest_timestamp(cls) -> 'Global':
        """Get the latest confirmed block UNIX timestamp.
        
        Fails if negative."""
        return cls(GlobalField.latest_timestamp)
    
    @classmethod
    def current_application_id(cls) -> 'Global':
        """Get the ID of the current application executing.
        
        Fails if no application is executing."""
        return cls(GlobalField.current_app_id)
    
    @classmethod
    def creator_address(cls) -> 'Global':
        """Address of the creator of the current application.
        
        Fails if no such application is executing. Requires TEAL version 3 or higher."""
        return cls(GlobalField.creator_address)

Global.__module__ = "pyteal"
