from datetime import date

from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.models.enums import ComponentType, OrderStatus


class Order(BaseModel):
    """Order entity - main order record"""
    __tablename__ = "orders"
    
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    order_date = Column(Date, nullable=False, index=True)
    delivery_date = Column(Date, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.QUOTE, nullable=False, index=True)
    
    # Pricing
    selling_price = Column(Numeric(10, 2), nullable=False)
    discount_amount = Column(Numeric(10, 2), default=0, nullable=False)
    tax_rate = Column(Numeric(5, 2), default=0, nullable=False)  # percentage
    tax_amount = Column(Numeric(10, 2), default=0, nullable=False)
    
    # Payment
    deposit_amount = Column(Numeric(10, 2), default=0, nullable=False)
    amount_paid = Column(Numeric(10, 2), default=0, nullable=False)
    amount_remaining = Column(Numeric(10, 2), default=0, nullable=False)
    
    # Costs
    estimated_total_cost = Column(Numeric(10, 2), nullable=False)
    actual_total_cost = Column(Numeric(10, 2), nullable=True)
    
    notes = Column(Text)
    
    # Relationships
    customer = relationship("Customer", back_populates="orders")
    components = relationship("OrderComponent", back_populates="order", cascade="all, delete-orphan")
    ingredient_usages = relationship("OrderIngredientUsage", back_populates="order", cascade="all, delete-orphan")
    supply_usages = relationship("OrderSupplyUsage", back_populates="order", cascade="all, delete-orphan")
    labor_entries = relationship("LaborEntry", back_populates="order", cascade="all, delete-orphan")
    operating_costs = relationship("OrderOperatingCost", back_populates="order", cascade="all, delete-orphan")
    cost_summary = relationship("OrderCostSummary", back_populates="order", uselist=False, cascade="all, delete-orphan")


class OrderComponent(BaseModel):
    """Order components - breakdown of what components make up the order"""
    __tablename__ = "order_components"
    
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    component_type = Column(Enum(ComponentType), nullable=False)
    recipe_variant_id = Column(Integer, ForeignKey("recipe_variants.id"), nullable=True)  # nullable for PACKAGING
    quantity = Column(Numeric(8, 2), nullable=False)
    notes = Column(Text)
    
    # Relationships
    order = relationship("Order", back_populates="components")
    recipe_variant = relationship("RecipeVariant", back_populates="order_components")


class OrderIngredientUsage(BaseModel):
    """Track ingredient usage for an order"""
    __tablename__ = "order_ingredient_usages"
    
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False, index=True)
    
    # Estimated values
    estimated_quantity = Column(Numeric(12, 2), nullable=False)
    estimated_cost = Column(Numeric(10, 2), nullable=False)
    
    # Actual values (filled when order is completed)
    actual_quantity = Column(Numeric(12, 2), nullable=True)
    actual_cost = Column(Numeric(10, 2), nullable=True)
    
    unit_used = Column(String(50), nullable=False)  # ingredient unit at time of order
    
    # Relationships
    order = relationship("Order", back_populates="ingredient_usages")
    ingredient = relationship("Ingredient", back_populates="order_ingredient_usages")


class OrderSupplyUsage(BaseModel):
    """Track supply usage for an order"""
    __tablename__ = "order_supply_usages"
    
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    supply_id = Column(Integer, ForeignKey("cake_supplies.id"), nullable=False, index=True)
    
    # Estimated values
    estimated_quantity = Column(Numeric(12, 2), nullable=False)
    estimated_cost = Column(Numeric(10, 2), nullable=False)
    
    # Actual values (filled when order is completed)
    actual_quantity = Column(Numeric(12, 2), nullable=True)
    actual_cost = Column(Numeric(10, 2), nullable=True)
    
    # Relationships
    order = relationship("Order", back_populates="supply_usages")
    supply = relationship("CakeSupply", back_populates="order_supply_usages")
