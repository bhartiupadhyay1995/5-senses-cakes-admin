from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Recipe(BaseModel):
    """Recipe base entity"""
    __tablename__ = "recipes"
    
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False)  # "Sponge", "Filling", "Frosting", "Decoration"
    description = Column(Text)
    active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Relationships
    variants = relationship("RecipeVariant", back_populates="recipe", cascade="all, delete-orphan")


class RecipeVariant(BaseModel):
    """Recipe variant - specific configuration like 6-inch 2-layer"""
    __tablename__ = "recipe_variants"
    
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False, index=True)
    variant_name = Column(String(255), nullable=False)  # "6-inch 2-layer"
    base_yield = Column(Numeric(8, 2), nullable=False)
    yield_unit = Column(String(50), nullable=False)  # "cake", "batch", "dozen"
    description = Column(Text)
    active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Relationships
    recipe = relationship("Recipe", back_populates="variants")
    ingredients = relationship("RecipeIngredient", back_populates="recipe_variant", cascade="all, delete-orphan")
    order_components = relationship("OrderComponent", back_populates="recipe_variant")


class RecipeIngredient(BaseModel):
    """Ingredients used in a recipe variant"""
    __tablename__ = "recipe_ingredients"
    
    recipe_variant_id = Column(Integer, ForeignKey("recipe_variants.id"), nullable=False, index=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False, index=True)
    quantity_required = Column(Numeric(12, 2), nullable=False)
    unit = Column(String(50), nullable=False)  # ingredient-specific unit
    
    # Relationships
    recipe_variant = relationship("RecipeVariant", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="recipe_ingredients")
