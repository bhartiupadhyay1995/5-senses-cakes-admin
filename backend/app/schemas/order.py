"""Order domain schemas"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from app.models.enums import ComponentType, OrderStatus


class OrderIngredientUsageBase(BaseModel):
    """Base order ingredient usage schema"""
    ingredient_id: int
    estimated_quantity: Decimal = Field(..., ge=0)
    estimated_cost: Decimal = Field(..., ge=0)
    actual_quantity: Optional[Decimal] = Field(None, ge=0)
    actual_cost: Optional[Decimal] = Field(None, ge=0)
    unit_used: str = Field(..., min_length=1, max_length=50)


class OrderIngredientUsageCreate(OrderIngredientUsageBase):
    """Order ingredient usage creation schema"""
    pass


class OrderIngredientUsageUpdate(BaseModel):
    """Order ingredient usage update schema"""
    actual_quantity: Optional[Decimal] = Field(None, ge=0)
    actual_cost: Optional[Decimal] = Field(None, ge=0)


class OrderIngredientUsageResponse(OrderIngredientUsageBase):
    """Order ingredient usage response schema"""
    id: int
    order_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderSupplyUsageBase(BaseModel):
    """Base order supply usage schema"""
    supply_id: int
    estimated_quantity: Decimal = Field(..., ge=0)
    estimated_cost: Decimal = Field(..., ge=0)
    actual_quantity: Optional[Decimal] = Field(None, ge=0)
    actual_cost: Optional[Decimal] = Field(None, ge=0)


class OrderSupplyUsageCreate(OrderSupplyUsageBase):
    """Order supply usage creation schema"""
    pass


class OrderSupplyUsageUpdate(BaseModel):
    """Order supply usage update schema"""
    actual_quantity: Optional[Decimal] = Field(None, ge=0)
    actual_cost: Optional[Decimal] = Field(None, ge=0)


class OrderSupplyUsageResponse(OrderSupplyUsageBase):
    """Order supply usage response schema"""
    id: int
    order_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderComponentBase(BaseModel):
    """Base order component schema"""
    component_type: ComponentType
    recipe_variant_id: Optional[int] = None
    quantity: Decimal = Field(..., gt=0)
    notes: Optional[str] = None


class OrderComponentCreate(OrderComponentBase):
    """Order component creation schema"""
    pass


class OrderComponentUpdate(BaseModel):
    """Order component update schema"""
    component_type: Optional[ComponentType] = None
    recipe_variant_id: Optional[int] = None
    quantity: Optional[Decimal] = Field(None, gt=0)
    notes: Optional[str] = None


class OrderComponentResponse(OrderComponentBase):
    """Order component response schema"""
    id: int
    order_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    """Base order schema"""
    customer_id: int
    order_date: date
    delivery_date: date
    status: OrderStatus = OrderStatus.QUOTE
    selling_price: Decimal = Field(..., ge=0)
    discount_amount: Decimal = Field(default=0, ge=0)
    tax_rate: Decimal = Field(default=0, ge=0, le=100)
    tax_amount: Decimal = Field(default=0, ge=0)
    deposit_amount: Decimal = Field(default=0, ge=0)
    amount_paid: Decimal = Field(default=0, ge=0)
    amount_remaining: Decimal = Field(default=0, ge=0)
    estimated_total_cost: Decimal = Field(..., ge=0)
    actual_total_cost: Optional[Decimal] = Field(None, ge=0)
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    """Order creation schema"""
    pass


class OrderUpdate(BaseModel):
    """Order update schema"""
    customer_id: Optional[int] = None
    order_date: Optional[date] = None
    delivery_date: Optional[date] = None
    status: Optional[OrderStatus] = None
    selling_price: Optional[Decimal] = Field(None, ge=0)
    discount_amount: Optional[Decimal] = Field(None, ge=0)
    tax_rate: Optional[Decimal] = Field(None, ge=0, le=100)
    tax_amount: Optional[Decimal] = Field(None, ge=0)
    deposit_amount: Optional[Decimal] = Field(None, ge=0)
    amount_paid: Optional[Decimal] = Field(None, ge=0)
    amount_remaining: Optional[Decimal] = Field(None, ge=0)
    estimated_total_cost: Optional[Decimal] = Field(None, ge=0)
    actual_total_cost: Optional[Decimal] = Field(None, ge=0)
    notes: Optional[str] = None


class OrderResponse(OrderBase):
    """Order response schema"""
    id: int
    components: Optional[list[OrderComponentResponse]] = None
    ingredient_usages: Optional[list[OrderIngredientUsageResponse]] = None
    supply_usages: Optional[list[OrderSupplyUsageResponse]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    """Order list response schema"""
    id: int
    customer_id: int
    order_date: date
    delivery_date: date
    status: OrderStatus
    selling_price: Decimal
    estimated_total_cost: Decimal
    actual_total_cost: Optional[Decimal]

    class Config:
        from_attributes = True
