"""Inventory domain schemas"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from app.models.enums import TransactionType


class IngredientUnitBase(BaseModel):
    """Base ingredient unit schema"""
    unit_name: str = Field(..., min_length=1, max_length=50)
    conversion_to_base: Decimal = Field(..., gt=0)


class IngredientUnitCreate(IngredientUnitBase):
    """Ingredient unit creation schema"""
    pass


class IngredientUnitResponse(IngredientUnitBase):
    """Ingredient unit response schema"""
    id: int
    ingredient_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IngredientBase(BaseModel):
    """Base ingredient schema"""
    name: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=100)
    base_unit: str = Field(..., min_length=1, max_length=20)
    current_cost_per_unit: Decimal = Field(..., gt=0)
    current_quantity: Decimal = Field(default=0, ge=0)
    min_threshold: Decimal = Field(default=0, ge=0)
    supplier: Optional[str] = Field(None, max_length=255)
    active: bool = True
    notes: Optional[str] = None


class IngredientCreate(IngredientBase):
    """Ingredient creation schema"""
    pass


class IngredientUpdate(BaseModel):
    """Ingredient update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    base_unit: Optional[str] = Field(None, min_length=1, max_length=20)
    current_cost_per_unit: Optional[Decimal] = Field(None, gt=0)
    current_quantity: Optional[Decimal] = Field(None, ge=0)
    min_threshold: Optional[Decimal] = Field(None, ge=0)
    supplier: Optional[str] = Field(None, max_length=255)
    active: Optional[bool] = None
    notes: Optional[str] = None


class IngredientResponse(IngredientBase):
    """Ingredient response schema"""
    id: int
    created_at: datetime
    updated_at: datetime
    units: Optional[list[IngredientUnitResponse]] = None

    class Config:
        from_attributes = True


class IngredientListResponse(BaseModel):
    """Ingredient list response schema"""
    id: int
    name: str
    category: str
    base_unit: str
    current_cost_per_unit: Decimal
    current_quantity: Decimal
    active: bool

    class Config:
        from_attributes = True


class InventoryTransactionBase(BaseModel):
    """Base inventory transaction schema"""
    ingredient_id: int
    transaction_type: TransactionType
    quantity_change: Decimal = Field(..., ne=0)
    transaction_date: date
    purchase_price_per_unit: Optional[Decimal] = Field(None, gt=0)
    notes: Optional[str] = None


class InventoryTransactionCreate(InventoryTransactionBase):
    """Inventory transaction creation schema"""
    pass


class InventoryTransactionResponse(InventoryTransactionBase):
    """Inventory transaction response schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CakeSupplyBase(BaseModel):
    """Base cake supply schema"""
    name: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=100)
    unit: str = Field(..., min_length=1, max_length=20)
    current_cost_per_unit: Decimal = Field(..., gt=0)
    current_quantity: Decimal = Field(default=0, ge=0)
    min_threshold: Decimal = Field(default=0, ge=0)
    supplier: Optional[str] = Field(None, max_length=255)
    active: bool = True
    notes: Optional[str] = None


class CakeSupplyCreate(CakeSupplyBase):
    """Cake supply creation schema"""
    pass


class CakeSupplyUpdate(BaseModel):
    """Cake supply update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    unit: Optional[str] = Field(None, min_length=1, max_length=20)
    current_cost_per_unit: Optional[Decimal] = Field(None, gt=0)
    current_quantity: Optional[Decimal] = Field(None, ge=0)
    min_threshold: Optional[Decimal] = Field(None, ge=0)
    supplier: Optional[str] = Field(None, max_length=255)
    active: Optional[bool] = None
    notes: Optional[str] = None


class CakeSupplyResponse(CakeSupplyBase):
    """Cake supply response schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CakeSupplyListResponse(BaseModel):
    """Cake supply list response schema"""
    id: int
    name: str
    category: str
    unit: str
    current_cost_per_unit: Decimal
    current_quantity: Decimal
    active: bool

    class Config:
        from_attributes = True


class SupplyTransactionBase(BaseModel):
    """Base supply transaction schema"""
    supply_id: int
    transaction_type: TransactionType
    quantity_change: Decimal = Field(..., ne=0)
    transaction_date: date
    purchase_price_per_unit: Optional[Decimal] = Field(None, gt=0)
    notes: Optional[str] = None


class SupplyTransactionCreate(SupplyTransactionBase):
    """Supply transaction creation schema"""
    pass


class SupplyTransactionResponse(SupplyTransactionBase):
    """Supply transaction response schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
