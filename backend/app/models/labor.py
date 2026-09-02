from sqlalchemy import Column, Enum, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.models.enums import Activity


class LaborEntry(BaseModel):
    """Labor activity tracking for orders"""
    __tablename__ = "labor_entries"
    
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    activity = Column(Enum(Activity), nullable=False)
    
    # Time tracking in minutes
    estimated_minutes = Column(Integer, nullable=False)
    actual_minutes = Column(Integer, nullable=True)
    
    # Hourly rate at time of recording
    hourly_rate = Column(Numeric(10, 2), nullable=False)
    
    notes = Column(Text)
    
    # Relationships
    order = relationship("Order", back_populates="labor_entries")
    
    @property
    def estimated_cost(self) -> float:
        """Calculate estimated labor cost"""
        return float(self.estimated_minutes) / 60 * float(self.hourly_rate)
    
    @property
    def actual_cost(self) -> float:
        """Calculate actual labor cost if actual_minutes is set"""
        if self.actual_minutes is None:
            return None
        return float(self.actual_minutes) / 60 * float(self.hourly_rate)
