from sqlalchemy import Boolean, Column, Date, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.models.enums import TransactionType


class Ingredient(BaseModel):
    """Ingredient model - Food items used in recipes"""
    __tablename__ = "ingredients"
    
    name = Column(String(255), nullable=False, unique=True, index=True)
    category = Column(String(100), nullable=False)  # "Dry", "Liquid", "Perishable", etc.
    base_unit = Column(String(20), nullable=False)  # "g", "ml", "cup", etc.
    current_cost_per_unit = Column(Numeric(10, 4), nullable=False)  # per base_unit
    current_quantity = Column(Numeric(12, 2), default=0, nullable=False)  # in base_unit
    min_threshold = Column(Numeric(12, 2), default=0, nullable=False)
    supplier = Column(String(255))
    active = Column(Boolean, default=True, nullable=False, index=True)
    notes = Column(Text)
    
    # Relationships
    transactions = relationship("InventoryTransaction", back_populates="ingredient", cascade="all, delete-orphan")
    recipe_ingredients = relationship("RecipeIngredient", back_populates="ingredient", cascade="all, delete-orphan")
    ingredient_units = relationship("IngredientUnit", back_populates="ingredient", cascade="all, delete-orphan")
    order_ingredient_usages = relationship("OrderIngredientUsage", back_populates="ingredient")


class IngredientUnit(BaseModel):
    """Support multiple units per ingredient"""
    __tablename__ = "ingredient_units"
    
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False, index=True)
    unit_name = Column(String(50), nullable=False)  # "cup", "oz", "tbsp", etc.
    conversion_to_base = Column(Numeric(12, 4), nullable=False)  # conversion factor to base unit
    
    # Relationships
    ingredient = relationship("Ingredient", back_populates="ingredient_units")


class InventoryTransaction(BaseModel):
    """Track all inventory movements"""
    __tablename__ = "inventory_transactions"
    
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False, index=True)
    transaction_type = Column(Enum(TransactionType), nullable=False, index=True)
    quantity_change = Column(Numeric(12, 2), nullable=False)  # signed (positive/negative)
    transaction_date = Column(Date, nullable=False, index=True)
    purchase_price_per_unit = Column(Numeric(10, 4))  # only for PURCHASE
    notes = Column(Text)
    
    # Relationships
    ingredient = relationship("Ingredient", back_populates="transactions")


class CakeSupply(BaseModel):
    """Non-food supplies (boxes, boards, toppers, etc.)"""
    __tablename__ = "cake_supplies"
    
    name = Column(String(255), nullable=False, unique=True, index=True)
    category = Column(String(100), nullable=False)
    unit = Column(String(20), nullable=False)  # "box", "board", "piece", etc.
    current_cost_per_unit = Column(Numeric(10, 4), nullable=False)
    current_quantity = Column(Numeric(12, 2), default=0, nullable=False)
    min_threshold = Column(Numeric(12, 2), default=0, nullable=False)
    supplier = Column(String(255))
    active = Column(Boolean, default=True, nullable=False, index=True)
    notes = Column(Text)
    
    # Relationships
    transactions = relationship("SupplyTransaction", back_populates="supply", cascade="all, delete-orphan")
    order_supply_usages = relationship("OrderSupplyUsage", back_populates="supply")
    order_components = relationship("OrderComponent", back_populates="supply")


class SupplyTransaction(BaseModel):
    """Track all supply movements"""
    __tablename__ = "supply_transactions"
    
    supply_id = Column(Integer, ForeignKey("cake_supplies.id"), nullable=False, index=True)
    transaction_type = Column(Enum(TransactionType), nullable=False, index=True)
    quantity_change = Column(Numeric(12, 2), nullable=False)
    transaction_date = Column(Date, nullable=False, index=True)
    purchase_price_per_unit = Column(Numeric(10, 4))
    notes = Column(Text)
    
    # Relationships
    supply = relationship("CakeSupply", back_populates="transactions")
