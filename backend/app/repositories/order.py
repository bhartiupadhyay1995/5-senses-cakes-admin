"""Order repositories"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import (
    Order,
    OrderComponent,
    OrderIngredientUsage,
    OrderOperatingCost,
    OrderSupplyUsage,
)
from app.models.enums import OrderStatus
from app.repositories.base import BaseRepository
from app.schemas.order import (
    OrderComponentCreate,
    OrderComponentUpdate,
    OrderCreate,
    OrderIngredientUsageCreate,
    OrderIngredientUsageUpdate,
    OrderSupplyUsageCreate,
    OrderSupplyUsageUpdate,
    OrderUpdate,
)


class OrderRepository(BaseRepository[Order, OrderCreate, OrderUpdate]):
    """Repository for Order entity"""

    def __init__(self, session: Session):
        super().__init__(session, Order)

    def get_by_customer(self, customer_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get orders for a specific customer"""
        return self.session.query(self.model_class).filter(
            Order.customer_id == customer_id
        ).offset(skip).limit(limit).order_by(Order.order_date.desc()).all()

    def get_by_status(self, status: OrderStatus, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get orders by status"""
        return self.session.query(self.model_class).filter(
            Order.status == status
        ).offset(skip).limit(limit).order_by(Order.order_date.desc()).all()

    def get_upcoming_deliveries(self, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get orders pending delivery"""
        return self.session.query(self.model_class).filter(
            Order.status.in_([OrderStatus.CONFIRMED, OrderStatus.IN_PROGRESS])
        ).offset(skip).limit(limit).order_by(Order.delivery_date).all()


class OrderComponentRepository(BaseRepository[OrderComponent, OrderComponentCreate, OrderComponentUpdate]):
    """Repository for OrderComponent entity"""

    def __init__(self, session: Session):
        super().__init__(session, OrderComponent)

    def get_by_order(self, order_id: int) -> List[OrderComponent]:
        """Get components for a specific order"""
        return self.session.query(self.model_class).filter(
            OrderComponent.order_id == order_id
        ).all()


class OrderIngredientUsageRepository(BaseRepository[OrderIngredientUsage, OrderIngredientUsageCreate, OrderIngredientUsageUpdate]):
    """Repository for OrderIngredientUsage entity"""

    def __init__(self, session: Session):
        super().__init__(session, OrderIngredientUsage)

    def get_by_order(self, order_id: int) -> List[OrderIngredientUsage]:
        """Get ingredient usages for a specific order"""
        return self.session.query(self.model_class).filter(
            OrderIngredientUsage.order_id == order_id
        ).all()

    def get_by_ingredient(self, ingredient_id: int, skip: int = 0, limit: int = 100) -> List[OrderIngredientUsage]:
        """Get orders using a specific ingredient"""
        return self.session.query(self.model_class).filter(
            OrderIngredientUsage.ingredient_id == ingredient_id
        ).offset(skip).limit(limit).all()


class OrderSupplyUsageRepository(BaseRepository[OrderSupplyUsage, OrderSupplyUsageCreate, OrderSupplyUsageUpdate]):
    """Repository for OrderSupplyUsage entity"""

    def __init__(self, session: Session):
        super().__init__(session, OrderSupplyUsage)

    def get_by_order(self, order_id: int) -> List[OrderSupplyUsage]:
        """Get supply usages for a specific order"""
        return self.session.query(self.model_class).filter(
            OrderSupplyUsage.order_id == order_id
        ).all()

    def get_by_supply(self, supply_id: int, skip: int = 0, limit: int = 100) -> List[OrderSupplyUsage]:
        """Get orders using a specific supply"""
        return self.session.query(self.model_class).filter(
            OrderSupplyUsage.supply_id == supply_id
        ).offset(skip).limit(limit).all()
