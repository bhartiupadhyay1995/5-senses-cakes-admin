"""Repository initialization and dependency injection"""

from sqlalchemy.orm import Session

from app.repositories.core import CustomerRepository, UserRepository
from app.repositories.cost import (
    LaborEntryRepository,
    OperatingCostCategoryRepository,
    OrderCostSummaryRepository,
    OrderOperatingCostRepository,
)
from app.repositories.inventory import (
    CakeSupplyRepository,
    IngredientRepository,
    InventoryTransactionRepository,
    SupplyTransactionRepository,
)
from app.repositories.order import (
    OrderComponentRepository,
    OrderIngredientUsageRepository,
    OrderRepository,
    OrderSupplyUsageRepository,
)
from app.repositories.recipe import (
    RecipeIngredientRepository,
    RecipeRepository,
    RecipeVariantRepository,
)


class RepositoryFactory:
    """Factory for creating repositories"""

    def __init__(self, session: Session):
        self.session = session

    # Core repositories
    @property
    def users(self) -> UserRepository:
        return UserRepository(self.session)

    @property
    def customers(self) -> CustomerRepository:
        return CustomerRepository(self.session)

    # Inventory repositories
    @property
    def ingredients(self) -> IngredientRepository:
        return IngredientRepository(self.session)

    @property
    def inventory_transactions(self) -> InventoryTransactionRepository:
        return InventoryTransactionRepository(self.session)

    @property
    def cake_supplies(self) -> CakeSupplyRepository:
        return CakeSupplyRepository(self.session)

    @property
    def supply_transactions(self) -> SupplyTransactionRepository:
        return SupplyTransactionRepository(self.session)

    # Recipe repositories
    @property
    def recipes(self) -> RecipeRepository:
        return RecipeRepository(self.session)

    @property
    def recipe_variants(self) -> RecipeVariantRepository:
        return RecipeVariantRepository(self.session)

    @property
    def recipe_ingredients(self) -> RecipeIngredientRepository:
        return RecipeIngredientRepository(self.session)

    # Order repositories
    @property
    def orders(self) -> OrderRepository:
        return OrderRepository(self.session)

    @property
    def order_components(self) -> OrderComponentRepository:
        return OrderComponentRepository(self.session)

    @property
    def order_ingredient_usages(self) -> OrderIngredientUsageRepository:
        return OrderIngredientUsageRepository(self.session)

    @property
    def order_supply_usages(self) -> OrderSupplyUsageRepository:
        return OrderSupplyUsageRepository(self.session)

    # Cost and labor repositories
    @property
    def labor_entries(self) -> LaborEntryRepository:
        return LaborEntryRepository(self.session)

    @property
    def operating_cost_categories(self) -> OperatingCostCategoryRepository:
        return OperatingCostCategoryRepository(self.session)

    @property
    def order_operating_costs(self) -> OrderOperatingCostRepository:
        return OrderOperatingCostRepository(self.session)

    @property
    def order_cost_summaries(self) -> OrderCostSummaryRepository:
        return OrderCostSummaryRepository(self.session)


def get_repository_factory(session: Session) -> RepositoryFactory:
    """Get repository factory for dependency injection"""
    return RepositoryFactory(session)
