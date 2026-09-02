"""Inventory repositories"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import CakeSupply, Ingredient, InventoryTransaction, SupplyTransaction
from app.models.enums import TransactionType
from app.repositories.base import BaseRepository
from app.schemas.inventory import (
    CakeSupplyCreate,
    CakeSupplyUpdate,
    IngredientCreate,
    IngredientUpdate,
    InventoryTransactionCreate,
    SupplyTransactionCreate,
)


class IngredientRepository(BaseRepository[Ingredient, IngredientCreate, IngredientUpdate]):
    """Repository for Ingredient entity"""

    def __init__(self, session: Session):
        super().__init__(session, Ingredient)

    def get_by_name(self, name: str) -> Optional[Ingredient]:
        """Get ingredient by name"""
        return self.session.query(self.model_class).filter(Ingredient.name == name).first()

    def get_active(self, skip: int = 0, limit: int = 100) -> List[Ingredient]:
        """Get active ingredients with pagination"""
        return self.session.query(self.model_class).filter(
            Ingredient.active == True
        ).offset(skip).limit(limit).all()

    def get_low_stock(self) -> List[Ingredient]:
        """Get ingredients below minimum threshold"""
        return self.session.query(self.model_class).filter(
            Ingredient.current_quantity <= Ingredient.min_threshold,
            Ingredient.active == True
        ).all()


class InventoryTransactionRepository(BaseRepository[InventoryTransaction, InventoryTransactionCreate, InventoryTransactionCreate]):
    """Repository for InventoryTransaction entity"""

    def __init__(self, session: Session):
        super().__init__(session, InventoryTransaction)

    def get_by_ingredient(self, ingredient_id: int, skip: int = 0, limit: int = 100) -> List[InventoryTransaction]:
        """Get transactions for a specific ingredient"""
        return self.session.query(self.model_class).filter(
            InventoryTransaction.ingredient_id == ingredient_id
        ).offset(skip).limit(limit).order_by(InventoryTransaction.transaction_date.desc()).all()

    def get_by_type(self, transaction_type: TransactionType, skip: int = 0, limit: int = 100) -> List[InventoryTransaction]:
        """Get transactions by type"""
        return self.session.query(self.model_class).filter(
            InventoryTransaction.transaction_type == transaction_type
        ).offset(skip).limit(limit).order_by(InventoryTransaction.transaction_date.desc()).all()


class CakeSupplyRepository(BaseRepository[CakeSupply, CakeSupplyCreate, CakeSupplyUpdate]):
    """Repository for CakeSupply entity"""

    def __init__(self, session: Session):
        super().__init__(session, CakeSupply)

    def get_by_name(self, name: str) -> Optional[CakeSupply]:
        """Get cake supply by name"""
        return self.session.query(self.model_class).filter(CakeSupply.name == name).first()

    def get_active(self, skip: int = 0, limit: int = 100) -> List[CakeSupply]:
        """Get active supplies with pagination"""
        return self.session.query(self.model_class).filter(
            CakeSupply.active == True
        ).offset(skip).limit(limit).all()

    def get_low_stock(self) -> List[CakeSupply]:
        """Get supplies below minimum threshold"""
        return self.session.query(self.model_class).filter(
            CakeSupply.current_quantity <= CakeSupply.min_threshold,
            CakeSupply.active == True
        ).all()


class SupplyTransactionRepository(BaseRepository[SupplyTransaction, SupplyTransactionCreate, SupplyTransactionCreate]):
    """Repository for SupplyTransaction entity"""

    def __init__(self, session: Session):
        super().__init__(session, SupplyTransaction)

    def get_by_supply(self, supply_id: int, skip: int = 0, limit: int = 100) -> List[SupplyTransaction]:
        """Get transactions for a specific supply"""
        return self.session.query(self.model_class).filter(
            SupplyTransaction.supply_id == supply_id
        ).offset(skip).limit(limit).order_by(SupplyTransaction.transaction_date.desc()).all()

    def get_by_type(self, transaction_type: TransactionType, skip: int = 0, limit: int = 100) -> List[SupplyTransaction]:
        """Get transactions by type"""
        return self.session.query(self.model_class).filter(
            SupplyTransaction.transaction_type == transaction_type
        ).offset(skip).limit(limit).order_by(SupplyTransaction.transaction_date.desc()).all()
