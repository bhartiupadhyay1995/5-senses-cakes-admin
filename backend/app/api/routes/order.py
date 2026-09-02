"""Order domain API routes"""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db_session
from app.api.errors import EntityNotFoundError
from app.models.enums import OrderStatus
from app.repositories import get_repository_factory
from app.schemas.order import (
    OrderComponentCreate,
    OrderComponentResponse,
    OrderComponentUpdate,
    OrderCreate,
    OrderIngredientUsageCreate,
    OrderIngredientUsageResponse,
    OrderIngredientUsageUpdate,
    OrderListResponse,
    OrderResponse,
    OrderSupplyUsageCreate,
    OrderSupplyUsageResponse,
    OrderSupplyUsageUpdate,
    OrderUpdate,
)

router = APIRouter()


# ============= Order Endpoints =============

@router.get("/orders", response_model=List[OrderListResponse])
def list_orders(
    session: Session = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
    customer_id: int = None,
    status: OrderStatus = None,
):
    """List all orders"""
    repos = get_repository_factory(session)
    
    if customer_id:
        return repos.orders.get_by_customer(customer_id, skip=skip, limit=limit)
    
    if status:
        return repos.orders.get_by_status(status, skip=skip, limit=limit)
    
    return repos.orders.get_all(skip=skip, limit=limit)


@router.get("/orders/upcoming-deliveries", response_model=List[OrderListResponse])
def get_upcoming_deliveries(
    session: Session = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
):
    """Get orders pending delivery"""
    repos = get_repository_factory(session)
    return repos.orders.get_upcoming_deliveries(skip=skip, limit=limit)


@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_in: OrderCreate,
    session: Session = Depends(get_db_session),
):
    """Create a new order"""
    repos = get_repository_factory(session)
    
    # Verify customer exists
    customer = repos.customers.get(order_in.customer_id)
    if not customer:
        raise EntityNotFoundError("Customer", order_in.customer_id)
    
    # Create order and cost summary
    order = repos.orders.create(order_in)
    repos.order_cost_summaries.create_for_order(order.id)
    
    return order


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    session: Session = Depends(get_db_session),
):
    """Get a specific order"""
    repos = get_repository_factory(session)
    order = repos.orders.get(order_id)
    if not order:
        raise EntityNotFoundError("Order", order_id)
    return order


@router.put("/orders/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_update: OrderUpdate,
    session: Session = Depends(get_db_session),
):
    """Update an order"""
    repos = get_repository_factory(session)
    
    order = repos.orders.get(order_id)
    if not order:
        raise EntityNotFoundError("Order", order_id)
    
    # Verify customer exists if updating customer
    if order_update.customer_id and order_update.customer_id != order.customer_id:
        customer = repos.customers.get(order_update.customer_id)
        if not customer:
            raise EntityNotFoundError("Customer", order_update.customer_id)
    
    return repos.orders.update(order_id, order_update)


@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    session: Session = Depends(get_db_session),
):
    """Delete an order"""
    repos = get_repository_factory(session)
    
    order = repos.orders.get(order_id)
    if not order:
        raise EntityNotFoundError("Order", order_id)
    
    repos.orders.delete(order_id)


# ============= Order Component Endpoints =============

@router.post("/orders/{order_id}/components", response_model=OrderComponentResponse, status_code=status.HTTP_201_CREATED)
def add_order_component(
    order_id: int,
    component_in: OrderComponentCreate,
    session: Session = Depends(get_db_session),
):
    """Add a component to an order"""
    repos = get_repository_factory(session)
    
    # Verify order exists
    order = repos.orders.get(order_id)
    if not order:
        raise EntityNotFoundError("Order", order_id)
    
    # If recipe_variant_id provided, verify it exists
    if component_in.recipe_variant_id:
        recipe_variant = repos.recipe_variants.get(component_in.recipe_variant_id)
        if not recipe_variant:
            raise EntityNotFoundError("RecipeVariant", component_in.recipe_variant_id)
    
    # Create component with order_id
    component_data = component_in.model_dump()
    component_data['order_id'] = order_id
    
    from app.models import OrderComponent
    order_component = OrderComponent(**component_data)
    session.add(order_component)
    session.commit()
    session.refresh(order_component)
    
    return order_component


@router.get("/orders/{order_id}/components", response_model=List[OrderComponentResponse])
def get_order_components(
    order_id: int,
    session: Session = Depends(get_db_session),
):
    """Get components for a specific order"""
    repos = get_repository_factory(session)
    
    # Verify order exists
    order = repos.orders.get(order_id)
    if not order:
        raise EntityNotFoundError("Order", order_id)
    
    return repos.order_components.get_by_order(order_id)


@router.put("/order-components/{component_id}", response_model=OrderComponentResponse)
def update_order_component(
    component_id: int,
    component_update: OrderComponentUpdate,
    session: Session = Depends(get_db_session),
):
    """Update an order component"""
    repos = get_repository_factory(session)
    
    component = repos.order_components.get(component_id)
    if not component:
        raise EntityNotFoundError("OrderComponent", component_id)
    
    return repos.order_components.update(component_id, component_update)


@router.delete("/order-components/{component_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_component(
    component_id: int,
    session: Session = Depends(get_db_session),
):
    """Delete an order component"""
    repos = get_repository_factory(session)
    
    component = repos.order_components.get(component_id)
    if not component:
        raise EntityNotFoundError("OrderComponent", component_id)
    
    repos.order_components.delete(component_id)


# ============= Order Ingredient Usage Endpoints =============

@router.post("/orders/{order_id}/ingredient-usages", response_model=OrderIngredientUsageResponse, status_code=status.HTTP_201_CREATED)
def add_order_ingredient_usage(
    order_id: int,
    usage_in: OrderIngredientUsageCreate,
    session: Session = Depends(get_db_session),
):
    """Add ingredient usage to an order"""
    repos = get_repository_factory(session)
    
    # Verify order exists
    order = repos.orders.get(order_id)
    if not order:
        raise EntityNotFoundError("Order", order_id)
    
    # Verify ingredient exists
    ingredient = repos.ingredients.get(usage_in.ingredient_id)
    if not ingredient:
        raise EntityNotFoundError("Ingredient", usage_in.ingredient_id)
    
    # Create usage with order_id
    usage_data = usage_in.model_dump()
    usage_data['order_id'] = order_id
    
    from app.models import OrderIngredientUsage
    order_usage = OrderIngredientUsage(**usage_data)
    session.add(order_usage)
    session.commit()
    session.refresh(order_usage)
    
    return order_usage


@router.get("/orders/{order_id}/ingredient-usages", response_model=List[OrderIngredientUsageResponse])
def get_order_ingredient_usages(
    order_id: int,
    session: Session = Depends(get_db_session),
):
    """Get ingredient usages for a specific order"""
    repos = get_repository_factory(session)
    
    # Verify order exists
    order = repos.orders.get(order_id)
    if not order:
        raise EntityNotFoundError("Order", order_id)
    
    return repos.order_ingredient_usages.get_by_order(order_id)


@router.put("/order-ingredient-usages/{usage_id}", response_model=OrderIngredientUsageResponse)
def update_order_ingredient_usage(
    usage_id: int,
    usage_update: OrderIngredientUsageUpdate,
    session: Session = Depends(get_db_session),
):
    """Update ingredient usage"""
    repos = get_repository_factory(session)
    
    usage = repos.order_ingredient_usages.get(usage_id)
    if not usage:
        raise EntityNotFoundError("OrderIngredientUsage", usage_id)
    
    return repos.order_ingredient_usages.update(usage_id, usage_update)


# ============= Order Supply Usage Endpoints =============

@router.post("/orders/{order_id}/supply-usages", response_model=OrderSupplyUsageResponse, status_code=status.HTTP_201_CREATED)
def add_order_supply_usage(
    order_id: int,
    usage_in: OrderSupplyUsageCreate,
    session: Session = Depends(get_db_session),
):
    """Add supply usage to an order"""
    repos = get_repository_factory(session)
    
    # Verify order exists
    order = repos.orders.get(order_id)
    if not order:
        raise EntityNotFoundError("Order", order_id)
    
    # Verify supply exists
    supply = repos.cake_supplies.get(usage_in.supply_id)
    if not supply:
        raise EntityNotFoundError("CakeSupply", usage_in.supply_id)
    
    # Create usage with order_id
    usage_data = usage_in.model_dump()
    usage_data['order_id'] = order_id
    
    from app.models import OrderSupplyUsage
    order_usage = OrderSupplyUsage(**usage_data)
    session.add(order_usage)
    session.commit()
    session.refresh(order_usage)
    
    return order_usage


@router.get("/orders/{order_id}/supply-usages", response_model=List[OrderSupplyUsageResponse])
def get_order_supply_usages(
    order_id: int,
    session: Session = Depends(get_db_session),
):
    """Get supply usages for a specific order"""
    repos = get_repository_factory(session)
    
    # Verify order exists
    order = repos.orders.get(order_id)
    if not order:
        raise EntityNotFoundError("Order", order_id)
    
    return repos.order_supply_usages.get_by_order(order_id)


@router.put("/order-supply-usages/{usage_id}", response_model=OrderSupplyUsageResponse)
def update_order_supply_usage(
    usage_id: int,
    usage_update: OrderSupplyUsageUpdate,
    session: Session = Depends(get_db_session),
):
    """Update supply usage"""
    repos = get_repository_factory(session)
    
    usage = repos.order_supply_usages.get(usage_id)
    if not usage:
        raise EntityNotFoundError("OrderSupplyUsage", usage_id)
    
    return repos.order_supply_usages.update(usage_id, usage_update)
