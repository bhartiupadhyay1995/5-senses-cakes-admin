"""API routes initialization and router registration"""

from fastapi import APIRouter

from app.api.routes.core import router as core_router
from app.api.routes.cost import router as cost_router
from app.api.routes.inventory import router as inventory_router
from app.api.routes.order import router as order_router
from app.api.routes.recipe import router as recipe_router

# Create main API router
api_router = APIRouter(prefix="/api/v1")

# Register route modules
api_router.include_router(core_router, tags=["core"])
api_router.include_router(inventory_router, tags=["inventory"])
api_router.include_router(recipe_router, tags=["recipes"])
api_router.include_router(order_router, tags=["orders"])
api_router.include_router(cost_router, tags=["costs", "labor"])

__all__ = ["api_router"]
