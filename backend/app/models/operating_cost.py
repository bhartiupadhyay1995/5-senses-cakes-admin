from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.models.enums import CostType


class OperatingCostCategory(BaseModel):
    """Categories for operating expenses"""
    __tablename__ = "operating_cost_categories"
    
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text)
    cost_type = Column(Enum(CostType), nullable=False)
    default_amount = Column(Numeric(10, 2), nullable=True)  # for FIXED_PER_ORDER types
    active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Relationships
    order_costs = relationship("OrderOperatingCost", back_populates="category", cascade="all, delete-orphan")


class OrderOperatingCost(BaseModel):
    """Operating costs associated with a specific order"""
    __tablename__ = "order_operating_costs"
    
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    operating_cost_category_id = Column(Integer, ForeignKey("operating_cost_categories.id"), nullable=False, index=True)
    
    # Estimated and actual amounts
    estimated_amount = Column(Numeric(10, 2), nullable=False)
    actual_amount = Column(Numeric(10, 2), nullable=True)
    
    notes = Column(Text)
    
    # Relationships
    order = relationship("Order", back_populates="operating_costs")
    category = relationship("OperatingCostCategory", back_populates="order_costs")


class OrderCostSummary(BaseModel):
    """Denormalized cost summary for quick access"""
    __tablename__ = "order_cost_summaries"
    
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True, unique=True)
    
    # Component costs
    ingredient_cost_estimated = Column(Numeric(10, 2), nullable=False, default=0)
    ingredient_cost_actual = Column(Numeric(10, 2), nullable=True)
    
    supply_cost_estimated = Column(Numeric(10, 2), nullable=False, default=0)
    supply_cost_actual = Column(Numeric(10, 2), nullable=True)
    
    labor_cost_estimated = Column(Numeric(10, 2), nullable=False, default=0)
    labor_cost_actual = Column(Numeric(10, 2), nullable=True)
    
    operating_cost_estimated = Column(Numeric(10, 2), nullable=False, default=0)
    operating_cost_actual = Column(Numeric(10, 2), nullable=True)
    
    # Totals
    total_cost_estimated = Column(Numeric(10, 2), nullable=False, default=0)
    total_cost_actual = Column(Numeric(10, 2), nullable=True)
    
    # Relationships
    order = relationship("Order", back_populates="cost_summary")
