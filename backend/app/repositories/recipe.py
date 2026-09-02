"""Recipe repositories"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Recipe, RecipeIngredient, RecipeVariant
from app.repositories.base import BaseRepository
from app.schemas.recipe import (
    RecipeCreate,
    RecipeIngredientCreate,
    RecipeUpdate,
    RecipeVariantCreate,
    RecipeVariantUpdate,
)


class RecipeRepository(BaseRepository[Recipe, RecipeCreate, RecipeUpdate]):
    """Repository for Recipe entity"""

    def __init__(self, session: Session):
        super().__init__(session, Recipe)

    def get_by_name(self, name: str) -> Optional[Recipe]:
        """Get recipe by name"""
        return self.session.query(self.model_class).filter(Recipe.name == name).first()

    def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Recipe]:
        """Get recipes by category"""
        return self.session.query(self.model_class).filter(
            Recipe.category == category
        ).offset(skip).limit(limit).all()

    def get_active(self, skip: int = 0, limit: int = 100) -> List[Recipe]:
        """Get active recipes"""
        return self.session.query(self.model_class).filter(
            Recipe.active == True
        ).offset(skip).limit(limit).all()


class RecipeVariantRepository(BaseRepository[RecipeVariant, RecipeVariantCreate, RecipeVariantUpdate]):
    """Repository for RecipeVariant entity"""

    def __init__(self, session: Session):
        super().__init__(session, RecipeVariant)

    def get_by_recipe(self, recipe_id: int) -> List[RecipeVariant]:
        """Get variants for a specific recipe"""
        return self.session.query(self.model_class).filter(
            RecipeVariant.recipe_id == recipe_id
        ).all()

    def get_active_by_recipe(self, recipe_id: int) -> List[RecipeVariant]:
        """Get active variants for a specific recipe"""
        return self.session.query(self.model_class).filter(
            RecipeVariant.recipe_id == recipe_id,
            RecipeVariant.active == True
        ).all()


class RecipeIngredientRepository(BaseRepository[RecipeIngredient, RecipeIngredientCreate, RecipeIngredientCreate]):
    """Repository for RecipeIngredient entity"""

    def __init__(self, session: Session):
        super().__init__(session, RecipeIngredient)

    def get_by_recipe_variant(self, recipe_variant_id: int) -> List[RecipeIngredient]:
        """Get ingredients for a specific recipe variant"""
        return self.session.query(self.model_class).filter(
            RecipeIngredient.recipe_variant_id == recipe_variant_id
        ).all()

    def get_by_ingredient(self, ingredient_id: int) -> List[RecipeIngredient]:
        """Get recipe usage for a specific ingredient"""
        return self.session.query(self.model_class).filter(
            RecipeIngredient.ingredient_id == ingredient_id
        ).all()
