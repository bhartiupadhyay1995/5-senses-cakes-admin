"""Cost and labor repositories"""

from typing import List

from sqlalchemy.orm import Session

from app.models import LaborEntry, OperatingCostCategory, OrderCostSummary, OrderOperatingCost
from app.repositories.base import BaseRepository
from app.schemas.cost import (
    OperatingCostCategoryCreate,
    OperatingCostCategoryUpdate,
    OrderOperatingCostCreate,
    OrderOperatingCostUpdate,
)
from app.schemas.labor import LaborEntryCreate, LaborEntryUpdate


class LaborEntryRepository(BaseRepository[LaborEntry, LaborEntryCreate, LaborEntryUpdate]):
    """Repository for LaborEntry entity"""

    def __init__(self, session: Session):
        super().__init__(session, LaborEntry)

    def get_by_order(self, order_id: int) -> List[LaborEntry]:
        """Get labor entries for a specific order"""
        return self.session.query(self.model_class).filter(
            LaborEntry.order_id == order_id
        ).all()


class OperatingCostCategoryRepository(BaseRepository[OperatingCostCategory, OperatingCostCategoryCreate, OperatingCostCategoryUpdate]):
    """Repository for OperatingCostCategory entity"""

    def __init__(self, session: Session):
        super().__init__(session, OperatingCostCategory)

    def get_by_name(self, name: str):
        """Get operating cost category by name"""
        return self.session.query(self.model_class).filter(
            OperatingCostCategory.name == name
        ).first()

    def get_active(self, skip: int = 0, limit: int = 100) -> List[OperatingCostCategory]:
        """Get active operating cost categories"""
        return self.session.query(self.model_class).filter(
            OperatingCostCategory.active == True
        ).offset(skip).limit(limit).all()


class OrderOperatingCostRepository(BaseRepository[OrderOperatingCost, OrderOperatingCostCreate, OrderOperatingCostUpdate]):
    """Repository for OrderOperatingCost entity"""

    def __init__(self, session: Session):
        super().__init__(session, OrderOperatingCost)

    def get_by_order(self, order_id: int) -> List[OrderOperatingCost]:
        """Get operating costs for a specific order"""
        return self.session.query(self.model_class).filter(
            OrderOperatingCost.order_id == order_id
        ).all()


class OrderCostSummaryRepository(BaseRepository[OrderCostSummary, OrderCostSummary, OrderCostSummary]):
    """Repository for OrderCostSummary entity"""

    def __init__(self, session: Session):
        super().__init__(session, OrderCostSummary)

    def get_by_order(self, order_id: int):
        """Get cost summary for a specific order"""
        return self.session.query(self.model_class).filter(
            OrderCostSummary.order_id == order_id
        ).first()

    def create_for_order(self, order_id: int) -> OrderCostSummary:
        """Create a cost summary for an order"""
        summary = OrderCostSummary(order_id=order_id)
        self.session.add(summary)
        self.session.commit()
        self.session.refresh(summary)
        return summary
