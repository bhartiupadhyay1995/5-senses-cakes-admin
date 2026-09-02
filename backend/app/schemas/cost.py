"""Cost domain schemas"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from app.models.enums import CostType


class OperatingCostCategoryBase(BaseModel):
    """Base operating cost category schema"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    cost_type: CostType
    default_amount: Optional[Decimal] = Field(None, ge=0)
    active: bool = True


class OperatingCostCategoryCreate(OperatingCostCategoryBase):
    """Operating cost category creation schema"""
    pass


class OperatingCostCategoryUpdate(BaseModel):
    """Operating cost category update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    cost_type: Optional[CostType] = None
    default_amount: Optional[Decimal] = Field(None, ge=0)
    active: Optional[bool] = None


class OperatingCostCategoryResponse(OperatingCostCategoryBase):
    """Operating cost category response schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderOperatingCostBase(BaseModel):
    """Base order operating cost schema"""
    operating_cost_category_id: int
    estimated_amount: Decimal = Field(..., ge=0)
    actual_amount: Optional[Decimal] = Field(None, ge=0)
    notes: Optional[str] = None


class OrderOperatingCostCreate(OrderOperatingCostBase):
    """Order operating cost creation schema"""
    pass


class OrderOperatingCostUpdate(BaseModel):
    """Order operating cost update schema"""
    estimated_amount: Optional[Decimal] = Field(None, ge=0)
    actual_amount: Optional[Decimal] = Field(None, ge=0)
    notes: Optional[str] = None


class OrderOperatingCostResponse(OrderOperatingCostBase):
    """Order operating cost response schema"""
    id: int
    order_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderCostSummaryBase(BaseModel):
    """Base order cost summary schema"""
    ingredient_cost_estimated: Decimal = Field(default=0, ge=0)
    ingredient_cost_actual: Optional[Decimal] = Field(None, ge=0)
    supply_cost_estimated: Decimal = Field(default=0, ge=0)
    supply_cost_actual: Optional[Decimal] = Field(None, ge=0)
    labor_cost_estimated: Decimal = Field(default=0, ge=0)
    labor_cost_actual: Optional[Decimal] = Field(None, ge=0)
    operating_cost_estimated: Decimal = Field(default=0, ge=0)
    operating_cost_actual: Optional[Decimal] = Field(None, ge=0)
    total_cost_estimated: Decimal = Field(default=0, ge=0)
    total_cost_actual: Optional[Decimal] = Field(None, ge=0)


class OrderCostSummaryResponse(OrderCostSummaryBase):
    """Order cost summary response schema"""
    id: int
    order_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
