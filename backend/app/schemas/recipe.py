"""Recipe domain schemas"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class RecipeIngredientBase(BaseModel):
    """Base recipe ingredient schema"""
    ingredient_id: int
    quantity_required: Decimal = Field(..., gt=0)
    unit: str = Field(..., min_length=1, max_length=50)


class RecipeIngredientCreate(RecipeIngredientBase):
    """Recipe ingredient creation schema"""
    pass


class RecipeIngredientResponse(RecipeIngredientBase):
    """Recipe ingredient response schema"""
    id: int
    recipe_variant_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RecipeVariantBase(BaseModel):
    """Base recipe variant schema"""
    variant_name: str = Field(..., min_length=1, max_length=255)
    base_yield: Decimal = Field(..., gt=0)
    yield_unit: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    active: bool = True


class RecipeVariantCreate(RecipeVariantBase):
    """Recipe variant creation schema"""
    recipe_id: int


class RecipeVariantUpdate(BaseModel):
    """Recipe variant update schema"""
    variant_name: Optional[str] = Field(None, min_length=1, max_length=255)
    base_yield: Optional[Decimal] = Field(None, gt=0)
    yield_unit: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    active: Optional[bool] = None


class RecipeVariantResponse(RecipeVariantBase):
    """Recipe variant response schema"""
    id: int
    recipe_id: int
    ingredients: Optional[list[RecipeIngredientResponse]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RecipeBase(BaseModel):
    """Base recipe schema"""
    name: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    active: bool = True


class RecipeCreate(RecipeBase):
    """Recipe creation schema"""
    pass


class RecipeUpdate(BaseModel):
    """Recipe update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    active: Optional[bool] = None


class RecipeResponse(RecipeBase):
    """Recipe response schema"""
    id: int
    variants: Optional[list[RecipeVariantResponse]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RecipeListResponse(BaseModel):
    """Recipe list response schema"""
    id: int
    name: str
    category: str
    active: bool

    class Config:
        from_attributes = True
