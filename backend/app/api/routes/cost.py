"""Cost and labor domain API routes"""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db_session
from app.api.errors import EntityAlreadyExistsError, EntityNotFoundError
from app.repositories import get_repository_factory
from app.schemas.cost import (
    OperatingCostCategoryCreate,
    OperatingCostCategoryResponse,
    OperatingCostCategoryUpdate,
    OrderCostSummaryResponse,
    OrderOperatingCostCreate,
    OrderOperatingCostResponse,
    OrderOperatingCostUpdate,
)
from app.schemas.labor import (
    LaborEntryCreate,
    LaborEntryResponse,
    LaborEntryUpdate,
)

router = APIRouter()


# ============= Labor Entry Endpoints =============

@router.post("/orders/{order_id}/labor-entries", response_model=LaborEntryResponse, status_code=status.HTTP_201_CREATED)
def add_labor_entry(
    order_id: int,
    labor_in: LaborEntryCreate,
    session: Session = Depends(get_db_session),
):
    """Add a labor entry to an order"""
    repos = get_repository_factory(session)
    
    # Verify order exists
    order = repos.orders.get(order_id)
    if not order:
        raise EntityNotFoundError("Order", order_id)
    
    # Ensure labor entry is for the correct order
    if labor_in.order_id != order_id:
        raise ValueError("Order ID mismatch")
    
    return repos.labor_entries.create(labor_in)


@router.get("/orders/{order_id}/labor-entries", response_model=List[LaborEntryResponse])
def get_labor_entries(
    order_id: int,
    session: Session = Depends(get_db_session),
):
    """Get labor entries for a specific order"""
    repos = get_repository_factory(session)
    
    # Verify order exists
    order = repos.orders.get(order_id)
    if not order:
        raise EntityNotFoundError("Order", order_id)
    
    return repos.labor_entries.get_by_order(order_id)


@router.put("/labor-entries/{labor_id}", response_model=LaborEntryResponse)
def update_labor_entry(
    labor_id: int,
    labor_update: LaborEntryUpdate,
    session: Session = Depends(get_db_session),
):
    """Update a labor entry"""
    repos = get_repository_factory(session)
    
    labor = repos.labor_entries.get(labor_id)
    if not labor:
        raise EntityNotFoundError("LaborEntry", labor_id)
    
    return repos.labor_entries.update(labor_id, labor_update)


@router.delete("/labor-entries/{labor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_labor_entry(
    labor_id: int,
    session: Session = Depends(get_db_session),
):
    """Delete a labor entry"""
    repos = get_repository_factory(session)
    
    labor = repos.labor_entries.get(labor_id)
    if not labor:
        raise EntityNotFoundError("LaborEntry", labor_id)
    
    repos.labor_entries.delete(labor_id)


# ============= Operating Cost Category Endpoints =============

@router.get("/operating-cost-categories", response_model=List[OperatingCostCategoryResponse])
def list_operating_cost_categories(
    session: Session = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
):
    """List all operating cost categories"""
    repos = get_repository_factory(session)
    
    if active_only:
        return repos.operating_cost_categories.get_active(skip=skip, limit=limit)
    
    return repos.operating_cost_categories.get_all(skip=skip, limit=limit)


@router.post("/operating-cost-categories", response_model=OperatingCostCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_operating_cost_category(
    category_in: OperatingCostCategoryCreate,
    session: Session = Depends(get_db_session),
):
    """Create a new operating cost category"""
    repos = get_repository_factory(session)
    
    # Check if category with name already exists
    existing = repos.operating_cost_categories.get_by_name(category_in.name)
    if existing:
        raise EntityAlreadyExistsError("OperatingCostCategory", "name", category_in.name)
    
    return repos.operating_cost_categories.create(category_in)


@router.get("/operating-cost-categories/{category_id}", response_model=OperatingCostCategoryResponse)
def get_operating_cost_category(
    category_id: int,
    session: Session = Depends(get_db_session),
):
    """Get a specific operating cost category"""
    repos = get_repository_factory(session)
    category = repos.operating_cost_categories.get(category_id)
    if not category:
        raise EntityNotFoundError("OperatingCostCategory", category_id)
    return category


@router.put("/operating-cost-categories/{category_id}", response_model=OperatingCostCategoryResponse)
def update_operating_cost_category(
    category_id: int,
    category_update: OperatingCostCategoryUpdate,
    session: Session = Depends(get_db_session),
):
    """Update an operating cost category"""
    repos = get_repository_factory(session)
    
    category = repos.operating_cost_categories.get(category_id)
    if not category:
        raise EntityNotFoundError("OperatingCostCategory", category_id)
    
    # Check if new name already exists (if name is being updated)
    if category_update.name and category_update.name != category.name:
        existing = repos.operating_cost_categories.get_by_name(category_update.name)
        if existing:
            raise EntityAlreadyExistsError("OperatingCostCategory", "name", category_update.name)
    
    return repos.operating_cost_categories.update(category_id, category_update)


@router.delete("/operating-cost-categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_operating_cost_category(
    category_id: int,
    session: Session = Depends(get_db_session),
):
    """Delete an operating cost category"""
    repos = get_repository_factory(session)
    
    category = repos.operating_cost_categories.get(category_id)
    if not category:
        raise EntityNotFoundError("OperatingCostCategory", category_id)
    
    repos.operating_cost_categories.delete(category_id)


# ============= Order Operating Cost Endpoints =============

@router.post("/orders/{order_id}/operating-costs", response_model=OrderOperatingCostResponse, status_code=status.HTTP_201_CREATED)
def add_order_operating_cost(
    order_id: int,
    cost_in: OrderOperatingCostCreate,
    session: Session = Depends(get_db_session),
):
    """Add an operating cost to an order"""
    repos = get_repository_factory(session)
    
    # Verify order exists
    order = repos.orders.get(order_id)
    if not order:
        raise EntityNotFoundError("Order", order_id)
    
    # Verify operating cost category exists
    category = repos.operating_cost_categories.get(cost_in.operating_cost_category_id)
    if not category:
        raise EntityNotFoundError("OperatingCostCategory", cost_in.operating_cost_category_id)
    
    # Create cost with order_id
    cost_data = cost_in.model_dump()
    cost_data['order_id'] = order_id
    
    from app.models import OrderOperatingCost
    order_cost = OrderOperatingCost(**cost_data)
    session.add(order_cost)
    session.commit()
    session.refresh(order_cost)
    
    return order_cost


@router.get("/orders/{order_id}/operating-costs", response_model=List[OrderOperatingCostResponse])
def get_order_operating_costs(
    order_id: int,
    session: Session = Depends(get_db_session),
):
    """Get operating costs for a specific order"""
    repos = get_repository_factory(session)
    
    # Verify order exists
    order = repos.orders.get(order_id)
    if not order:
        raise EntityNotFoundError("Order", order_id)
    
    return repos.order_operating_costs.get_by_order(order_id)


@router.put("/order-operating-costs/{cost_id}", response_model=OrderOperatingCostResponse)
def update_order_operating_cost(
    cost_id: int,
    cost_update: OrderOperatingCostUpdate,
    session: Session = Depends(get_db_session),
):
    """Update an order operating cost"""
    repos = get_repository_factory(session)
    
    cost = repos.order_operating_costs.get(cost_id)
    if not cost:
        raise EntityNotFoundError("OrderOperatingCost", cost_id)
    
    return repos.order_operating_costs.update(cost_id, cost_update)


@router.delete("/order-operating-costs/{cost_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_operating_cost(
    cost_id: int,
    session: Session = Depends(get_db_session),
):
    """Delete an order operating cost"""
    repos = get_repository_factory(session)
    
    cost = repos.order_operating_costs.get(cost_id)
    if not cost:
        raise EntityNotFoundError("OrderOperatingCost", cost_id)
    
    repos.order_operating_costs.delete(cost_id)


# ============= Order Cost Summary Endpoints =============

@router.get("/orders/{order_id}/cost-summary", response_model=OrderCostSummaryResponse)
def get_order_cost_summary(
    order_id: int,
    session: Session = Depends(get_db_session),
):
    """Get cost summary for a specific order"""
    repos = get_repository_factory(session)
    
    # Verify order exists
    order = repos.orders.get(order_id)
    if not order:
        raise EntityNotFoundError("Order", order_id)
    
    summary = repos.order_cost_summaries.get_by_order(order_id)
    if not summary:
        raise EntityNotFoundError("OrderCostSummary", order_id)
    
    return summary
