"""Inventory domain API routes"""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db_session
from app.api.errors import EntityAlreadyExistsError, EntityNotFoundError
from app.repositories import get_repository_factory
from app.schemas.inventory import (
    CakeSupplyCreate,
    CakeSupplyListResponse,
    CakeSupplyResponse,
    CakeSupplyUpdate,
    IngredientCreate,
    IngredientListResponse,
    IngredientResponse,
    IngredientUpdate,
    InventoryTransactionCreate,
    InventoryTransactionResponse,
    SupplyTransactionCreate,
    SupplyTransactionResponse,
)

router = APIRouter()


# ============= Ingredient Endpoints =============

@router.get("/ingredients", response_model=List[IngredientListResponse])
def list_ingredients(
    session: Session = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
):
    """List all ingredients"""
    repos = get_repository_factory(session)
    
    if active_only:
        return repos.ingredients.get_active(skip=skip, limit=limit)
    
    return repos.ingredients.get_all(skip=skip, limit=limit)


@router.get("/ingredients/low-stock", response_model=List[IngredientListResponse])
def list_low_stock_ingredients(session: Session = Depends(get_db_session)):
    """List ingredients below minimum threshold"""
    repos = get_repository_factory(session)
    return repos.ingredients.get_low_stock()


@router.post("/ingredients", response_model=IngredientResponse, status_code=status.HTTP_201_CREATED)
def create_ingredient(
    ingredient_in: IngredientCreate,
    session: Session = Depends(get_db_session),
):
    """Create a new ingredient"""
    repos = get_repository_factory(session)
    
    # Check if ingredient with name already exists
    existing = repos.ingredients.get_by_name(ingredient_in.name)
    if existing:
        raise EntityAlreadyExistsError("Ingredient", "name", ingredient_in.name)
    
    return repos.ingredients.create(ingredient_in)


@router.get("/ingredients/{ingredient_id}", response_model=IngredientResponse)
def get_ingredient(
    ingredient_id: int,
    session: Session = Depends(get_db_session),
):
    """Get a specific ingredient"""
    repos = get_repository_factory(session)
    ingredient = repos.ingredients.get(ingredient_id)
    if not ingredient:
        raise EntityNotFoundError("Ingredient", ingredient_id)
    return ingredient


@router.put("/ingredients/{ingredient_id}", response_model=IngredientResponse)
def update_ingredient(
    ingredient_id: int,
    ingredient_update: IngredientUpdate,
    session: Session = Depends(get_db_session),
):
    """Update an ingredient"""
    repos = get_repository_factory(session)
    
    ingredient = repos.ingredients.get(ingredient_id)
    if not ingredient:
        raise EntityNotFoundError("Ingredient", ingredient_id)
    
    # Check if new name already exists (if name is being updated)
    if ingredient_update.name and ingredient_update.name != ingredient.name:
        existing = repos.ingredients.get_by_name(ingredient_update.name)
        if existing:
            raise EntityAlreadyExistsError("Ingredient", "name", ingredient_update.name)
    
    return repos.ingredients.update(ingredient_id, ingredient_update)


@router.delete("/ingredients/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(
    ingredient_id: int,
    session: Session = Depends(get_db_session),
):
    """Delete an ingredient"""
    repos = get_repository_factory(session)
    
    ingredient = repos.ingredients.get(ingredient_id)
    if not ingredient:
        raise EntityNotFoundError("Ingredient", ingredient_id)
    
    repos.ingredients.delete(ingredient_id)


# ============= Inventory Transaction Endpoints =============

@router.post("/ingredients/{ingredient_id}/transactions", response_model=InventoryTransactionResponse, status_code=status.HTTP_201_CREATED)
def record_inventory_transaction(
    ingredient_id: int,
    transaction_in: InventoryTransactionCreate,
    session: Session = Depends(get_db_session),
):
    """Record an inventory transaction"""
    repos = get_repository_factory(session)
    
    # Verify ingredient exists
    ingredient = repos.ingredients.get(ingredient_id)
    if not ingredient:
        raise EntityNotFoundError("Ingredient", ingredient_id)
    
    # Ensure transaction is for the correct ingredient
    if transaction_in.ingredient_id != ingredient_id:
        raise ValueError("Ingredient ID mismatch")
    
    return repos.inventory_transactions.create(transaction_in)


@router.get("/ingredients/{ingredient_id}/transactions", response_model=List[InventoryTransactionResponse])
def get_ingredient_transactions(
    ingredient_id: int,
    session: Session = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
):
    """Get inventory transactions for a specific ingredient"""
    repos = get_repository_factory(session)
    
    # Verify ingredient exists
    ingredient = repos.ingredients.get(ingredient_id)
    if not ingredient:
        raise EntityNotFoundError("Ingredient", ingredient_id)
    
    return repos.inventory_transactions.get_by_ingredient(ingredient_id, skip=skip, limit=limit)


# ============= Cake Supply Endpoints =============

@router.get("/supplies", response_model=List[CakeSupplyListResponse])
def list_supplies(
    session: Session = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
):
    """List all cake supplies"""
    repos = get_repository_factory(session)
    
    if active_only:
        return repos.cake_supplies.get_active(skip=skip, limit=limit)
    
    return repos.cake_supplies.get_all(skip=skip, limit=limit)


@router.get("/supplies/low-stock", response_model=List[CakeSupplyListResponse])
def list_low_stock_supplies(session: Session = Depends(get_db_session)):
    """List supplies below minimum threshold"""
    repos = get_repository_factory(session)
    return repos.cake_supplies.get_low_stock()


@router.post("/supplies", response_model=CakeSupplyResponse, status_code=status.HTTP_201_CREATED)
def create_supply(
    supply_in: CakeSupplyCreate,
    session: Session = Depends(get_db_session),
):
    """Create a new cake supply"""
    repos = get_repository_factory(session)
    
    # Check if supply with name already exists
    existing = repos.cake_supplies.get_by_name(supply_in.name)
    if existing:
        raise EntityAlreadyExistsError("CakeSupply", "name", supply_in.name)
    
    return repos.cake_supplies.create(supply_in)


@router.get("/supplies/{supply_id}", response_model=CakeSupplyResponse)
def get_supply(
    supply_id: int,
    session: Session = Depends(get_db_session),
):
    """Get a specific cake supply"""
    repos = get_repository_factory(session)
    supply = repos.cake_supplies.get(supply_id)
    if not supply:
        raise EntityNotFoundError("CakeSupply", supply_id)
    return supply


@router.put("/supplies/{supply_id}", response_model=CakeSupplyResponse)
def update_supply(
    supply_id: int,
    supply_update: CakeSupplyUpdate,
    session: Session = Depends(get_db_session),
):
    """Update a cake supply"""
    repos = get_repository_factory(session)
    
    supply = repos.cake_supplies.get(supply_id)
    if not supply:
        raise EntityNotFoundError("CakeSupply", supply_id)
    
    # Check if new name already exists (if name is being updated)
    if supply_update.name and supply_update.name != supply.name:
        existing = repos.cake_supplies.get_by_name(supply_update.name)
        if existing:
            raise EntityAlreadyExistsError("CakeSupply", "name", supply_update.name)
    
    return repos.cake_supplies.update(supply_id, supply_update)


@router.delete("/supplies/{supply_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supply(
    supply_id: int,
    session: Session = Depends(get_db_session),
):
    """Delete a cake supply"""
    repos = get_repository_factory(session)
    
    supply = repos.cake_supplies.get(supply_id)
    if not supply:
        raise EntityNotFoundError("CakeSupply", supply_id)
    
    repos.cake_supplies.delete(supply_id)


# ============= Supply Transaction Endpoints =============

@router.post("/supplies/{supply_id}/transactions", response_model=SupplyTransactionResponse, status_code=status.HTTP_201_CREATED)
def record_supply_transaction(
    supply_id: int,
    transaction_in: SupplyTransactionCreate,
    session: Session = Depends(get_db_session),
):
    """Record a supply transaction"""
    repos = get_repository_factory(session)
    
    # Verify supply exists
    supply = repos.cake_supplies.get(supply_id)
    if not supply:
        raise EntityNotFoundError("CakeSupply", supply_id)
    
    # Ensure transaction is for the correct supply
    if transaction_in.supply_id != supply_id:
        raise ValueError("Supply ID mismatch")
    
    return repos.supply_transactions.create(transaction_in)


@router.get("/supplies/{supply_id}/transactions", response_model=List[SupplyTransactionResponse])
def get_supply_transactions(
    supply_id: int,
    session: Session = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
):
    """Get supply transactions for a specific supply"""
    repos = get_repository_factory(session)
    
    # Verify supply exists
    supply = repos.cake_supplies.get(supply_id)
    if not supply:
        raise EntityNotFoundError("CakeSupply", supply_id)
    
    return repos.supply_transactions.get_by_supply(supply_id, skip=skip, limit=limit)
