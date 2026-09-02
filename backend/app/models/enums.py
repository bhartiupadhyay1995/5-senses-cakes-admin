from enum import Enum


class TransactionType(str, Enum):
    """Inventory transaction types"""
    PURCHASE = "PURCHASE"
    CONSUMPTION = "CONSUMPTION"
    ADJUSTMENT = "ADJUSTMENT"
    WASTE = "WASTE"
    RETURN = "RETURN"


class OrderStatus(str, Enum):
    """Order lifecycle statuses"""
    QUOTE = "QUOTE"
    CONFIRMED = "CONFIRMED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class ComponentType(str, Enum):
    """Order component types"""
    SPONGE = "SPONGE"
    FILLING = "FILLING"
    FROSTING = "FROSTING"
    DECORATION = "DECORATION"
    PACKAGING = "PACKAGING"


class Activity(str, Enum):
    """Labor activities"""
    PREP = "PREP"
    BAKING = "BAKING"
    FILLING = "FILLING"
    FROSTING = "FROSTING"
    DECORATION = "DECORATION"
    CLEANUP = "CLEANUP"


class CostType(str, Enum):
    """Operating cost types"""
    FIXED_PER_ORDER = "FIXED_PER_ORDER"
    USAGE_BASED = "USAGE_BASED"


class PaymentMethod(str, Enum):
    """Payment methods"""
    CASH = "CASH"
    CARD = "CARD"
    BANK_TRANSFER = "BANK_TRANSFER"
    CHECK = "CHECK"
    OTHER = "OTHER"
