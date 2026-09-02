"""Recipe domain API routes"""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db_session
from app.api.errors import EntityAlreadyExistsError, EntityNotFoundError
from app.repositories import get_repository_factory
from app.schemas.recipe import (
    RecipeCreate,
    RecipeIngredientCreate,
    RecipeIngredientResponse,
    RecipeListResponse,
    RecipeResponse,
    RecipeUpdate,
    RecipeVariantCreate,
    RecipeVariantResponse,
    RecipeVariantUpdate,
)

router = APIRouter()


# ============= Recipe Endpoints =============

@router.get("/recipes", response_model=List[RecipeListResponse])
def list_recipes(
    session: Session = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    category: str = None,
):
    """List all recipes"""
    repos = get_repository_factory(session)
    
    if category:
        return repos.recipes.get_by_category(category, skip=skip, limit=limit)
    
    if active_only:
        return repos.recipes.get_active(skip=skip, limit=limit)
    
    return repos.recipes.get_all(skip=skip, limit=limit)


@router.post("/recipes", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def create_recipe(
    recipe_in: RecipeCreate,
    session: Session = Depends(get_db_session),
):
    """Create a new recipe"""
    repos = get_repository_factory(session)
    
    # Check if recipe with name already exists
    existing = repos.recipes.get_by_name(recipe_in.name)
    if existing:
        raise EntityAlreadyExistsError("Recipe", "name", recipe_in.name)
    
    return repos.recipes.create(recipe_in)


@router.get("/recipes/{recipe_id}", response_model=RecipeResponse)
def get_recipe(
    recipe_id: int,
    session: Session = Depends(get_db_session),
):
    """Get a specific recipe"""
    repos = get_repository_factory(session)
    recipe = repos.recipes.get(recipe_id)
    if not recipe:
        raise EntityNotFoundError("Recipe", recipe_id)
    return recipe


@router.put("/recipes/{recipe_id}", response_model=RecipeResponse)
def update_recipe(
    recipe_id: int,
    recipe_update: RecipeUpdate,
    session: Session = Depends(get_db_session),
):
    """Update a recipe"""
    repos = get_repository_factory(session)
    
    recipe = repos.recipes.get(recipe_id)
    if not recipe:
        raise EntityNotFoundError("Recipe", recipe_id)
    
    # Check if new name already exists (if name is being updated)
    if recipe_update.name and recipe_update.name != recipe.name:
        existing = repos.recipes.get_by_name(recipe_update.name)
        if existing:
            raise EntityAlreadyExistsError("Recipe", "name", recipe_update.name)
    
    return repos.recipes.update(recipe_id, recipe_update)


@router.delete("/recipes/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    recipe_id: int,
    session: Session = Depends(get_db_session),
):
    """Delete a recipe"""
    repos = get_repository_factory(session)
    
    recipe = repos.recipes.get(recipe_id)
    if not recipe:
        raise EntityNotFoundError("Recipe", recipe_id)
    
    repos.recipes.delete(recipe_id)


# ============= Recipe Variant Endpoints =============

@router.post("/recipes/{recipe_id}/variants", response_model=RecipeVariantResponse, status_code=status.HTTP_201_CREATED)
def create_recipe_variant(
    recipe_id: int,
    variant_in: RecipeVariantCreate,
    session: Session = Depends(get_db_session),
):
    """Create a new recipe variant"""
    repos = get_repository_factory(session)
    
    # Verify recipe exists
    recipe = repos.recipes.get(recipe_id)
    if not recipe:
        raise EntityNotFoundError("Recipe", recipe_id)
    
    # Ensure variant is for the correct recipe
    if variant_in.recipe_id != recipe_id:
        raise ValueError("Recipe ID mismatch")
    
    return repos.recipe_variants.create(variant_in)


@router.get("/recipes/{recipe_id}/variants", response_model=List[RecipeVariantResponse])
def list_recipe_variants(
    recipe_id: int,
    session: Session = Depends(get_db_session),
):
    """List variants for a specific recipe"""
    repos = get_repository_factory(session)
    
    # Verify recipe exists
    recipe = repos.recipes.get(recipe_id)
    if not recipe:
        raise EntityNotFoundError("Recipe", recipe_id)
    
    return repos.recipe_variants.get_by_recipe(recipe_id)


@router.get("/recipe-variants/{variant_id}", response_model=RecipeVariantResponse)
def get_recipe_variant(
    variant_id: int,
    session: Session = Depends(get_db_session),
):
    """Get a specific recipe variant"""
    repos = get_repository_factory(session)
    variant = repos.recipe_variants.get(variant_id)
    if not variant:
        raise EntityNotFoundError("RecipeVariant", variant_id)
    return variant


@router.put("/recipe-variants/{variant_id}", response_model=RecipeVariantResponse)
def update_recipe_variant(
    variant_id: int,
    variant_update: RecipeVariantUpdate,
    session: Session = Depends(get_db_session),
):
    """Update a recipe variant"""
    repos = get_repository_factory(session)
    
    variant = repos.recipe_variants.get(variant_id)
    if not variant:
        raise EntityNotFoundError("RecipeVariant", variant_id)
    
    return repos.recipe_variants.update(variant_id, variant_update)


@router.delete("/recipe-variants/{variant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe_variant(
    variant_id: int,
    session: Session = Depends(get_db_session),
):
    """Delete a recipe variant"""
    repos = get_repository_factory(session)
    
    variant = repos.recipe_variants.get(variant_id)
    if not variant:
        raise EntityNotFoundError("RecipeVariant", variant_id)
    
    repos.recipe_variants.delete(variant_id)


# ============= Recipe Ingredient Endpoints =============

@router.post("/recipe-variants/{variant_id}/ingredients", response_model=RecipeIngredientResponse, status_code=status.HTTP_201_CREATED)
def add_recipe_ingredient(
    variant_id: int,
    ingredient_in: RecipeIngredientCreate,
    session: Session = Depends(get_db_session),
):
    """Add an ingredient to a recipe variant"""
    repos = get_repository_factory(session)
    
    # Verify variant exists
    variant = repos.recipe_variants.get(variant_id)
    if not variant:
        raise EntityNotFoundError("RecipeVariant", variant_id)
    
    # Verify ingredient exists
    ingredient = repos.ingredients.get(ingredient_in.ingredient_id)
    if not ingredient:
        raise EntityNotFoundError("Ingredient", ingredient_in.ingredient_id)
    
    # Create recipe ingredient with variant_id
    ingredient_data = ingredient_in.model_dump()
    ingredient_data['recipe_variant_id'] = variant_id
    
    from app.models import RecipeIngredient
    recipe_ingredient = RecipeIngredient(**ingredient_data)
    session.add(recipe_ingredient)
    session.commit()
    session.refresh(recipe_ingredient)
    
    return recipe_ingredient


@router.get("/recipe-variants/{variant_id}/ingredients", response_model=List[RecipeIngredientResponse])
def get_recipe_ingredients(
    variant_id: int,
    session: Session = Depends(get_db_session),
):
    """Get ingredients for a specific recipe variant"""
    repos = get_repository_factory(session)
    
    # Verify variant exists
    variant = repos.recipe_variants.get(variant_id)
    if not variant:
        raise EntityNotFoundError("RecipeVariant", variant_id)
    
    return repos.recipe_ingredients.get_by_recipe_variant(variant_id)


@router.delete("/recipe-ingredients/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_recipe_ingredient(
    ingredient_id: int,
    session: Session = Depends(get_db_session),
):
    """Remove an ingredient from a recipe variant"""
    repos = get_repository_factory(session)
    
    recipe_ingredient = repos.recipe_ingredients.get(ingredient_id)
    if not recipe_ingredient:
        raise EntityNotFoundError("RecipeIngredient", ingredient_id)
    
    repos.recipe_ingredients.delete(ingredient_id)
