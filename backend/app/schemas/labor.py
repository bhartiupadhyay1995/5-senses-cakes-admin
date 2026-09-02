"""Labor domain schemas"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from app.models.enums import Activity


class LaborEntryBase(BaseModel):
    """Base labor entry schema"""
    order_id: int
    activity: Activity
    estimated_minutes: int = Field(..., gt=0)
    actual_minutes: Optional[int] = Field(None, gt=0)
    hourly_rate: Decimal = Field(..., gt=0)
    notes: Optional[str] = None


class LaborEntryCreate(LaborEntryBase):
    """Labor entry creation schema"""
    pass


class LaborEntryUpdate(BaseModel):
    """Labor entry update schema"""
    activity: Optional[Activity] = None
    estimated_minutes: Optional[int] = Field(None, gt=0)
    actual_minutes: Optional[int] = Field(None, gt=0)
    hourly_rate: Optional[Decimal] = Field(None, gt=0)
    notes: Optional[str] = None


class LaborEntryResponse(LaborEntryBase):
    """Labor entry response schema"""
    id: int
    estimated_cost: Optional[Decimal] = None
    actual_cost: Optional[Decimal] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @property
    def estimated_cost_calc(self) -> Decimal:
        """Calculate estimated labor cost"""
        return Decimal(self.estimated_minutes) / 60 * self.hourly_rate

    @property
    def actual_cost_calc(self) -> Optional[Decimal]:
        """Calculate actual labor cost if actual_minutes is set"""
        if self.actual_minutes is None:
            return None
        return Decimal(self.actual_minutes) / 60 * self.hourly_rate
