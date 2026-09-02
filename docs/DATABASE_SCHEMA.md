# Database Schema Design
## 5 Senses Cakes

---

## 1. Entity Relationship Diagram (Conceptual)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CORE INVENTORY ENTITIES                         │
├─────────────────────────────────────────────────────────────────────────┤

User (single-user app, auth-ready)
├── id (PK)
├── name
├── email
├── hourly_rate (DECIMAL)
├── created_at, updated_at

Ingredient
├── id (PK)
├── name
├── category
├── base_unit (e.g., "g", "ml", "cup")
├── current_cost_per_unit (DECIMAL)
├── current_quantity (DECIMAL)
├── min_threshold (DECIMAL)
├── supplier
├── active
├── created_at, updated_at

IngredientUnit (supports multiple units per ingredient)
├── id (PK)
├── ingredient_id (FK)
├── unit_name (e.g., "cup", "oz", "tbsp")
├── conversion_to_base (e.g., 240 ml = 1 cup)

InventoryTransaction
├── id (PK)
├── ingredient_id (FK)
├── transaction_type (ENUM: PURCHASE, CONSUMPTION, ADJUSTMENT, WASTE, RETURN)
├── quantity_change (DECIMAL, signed)
├── transaction_date
├── purchase_price_per_unit (DECIMAL, optional)
├── notes
├── created_at

CakeSupply (non-food items like boxes, boards, toppers, etc.)
├── id (PK)
├── name
├── category
├── unit (e.g., "box", "board", "piece")
├── current_cost_per_unit (DECIMAL)
├── current_quantity (DECIMAL)
├── min_threshold (DECIMAL)
├── supplier
├── active
├── created_at, updated_at

SupplyTransaction (similar to inventory transactions)
├── id (PK)
├── supply_id (FK)
├── transaction_type
├── quantity_change
├── transaction_date
├── purchase_price_per_unit
├── notes
├── created_at

├─────────────────────────────────────────────────────────────────────────┤
│                        RECIPE ENTITIES                                  │
├─────────────────────────────────────────────────────────────────────────┤

Recipe
├── id (PK)
├── name
├── category (e.g., "Sponge", "Filling", "Frosting", "Decoration")
├── description
├── active
├── created_at, updated_at

RecipeVariant
├── id (PK)
├── recipe_id (FK)
├── variant_name (e.g., "6-inch 2-layer", "8-inch 3-layer")
├── base_yield (DECIMAL)
├── yield_unit (e.g., "cake", "batch")
├── description
├── active
├── created_at, updated_at

RecipeIngredient
├── id (PK)
├── recipe_variant_id (FK)
├── ingredient_id (FK)
├── quantity_required (DECIMAL)
├── unit (ingredient-specific unit, e.g., "g", "cup", "ml")

├─────────────────────────────────────────────────────────────────────────┤
│                        CUSTOMER & ORDER ENTITIES                        │
├─────────────────────────────────────────────────────────────────────────┤

Customer
├── id (PK)
├── name
├── email
├── phone
├── address
├── notes (dietary restrictions, preferences)
├── created_at, updated_at

Order
├── id (PK)
├── customer_id (FK)
├── order_date
├── delivery_date
├── status (ENUM: QUOTE, CONFIRMED, IN_PROGRESS, COMPLETED, CANCELLED)
├── selling_price (DECIMAL)
├── discount_amount (DECIMAL)
├── tax_rate (DECIMAL, default 0)
├── tax_amount (DECIMAL)
├── deposit_amount (DECIMAL)
├── amount_paid (DECIMAL)
├── amount_remaining (DECIMAL)
├── estimated_total_cost (DECIMAL, calculated)
├── actual_total_cost (DECIMAL, updated when completed)
├── notes
├── created_at, updated_at

OrderComponent (many components per order)
├── id (PK)
├── order_id (FK)
├── component_type (ENUM: SPONGE, FILLING, FROSTING, DECORATION, PACKAGING)
├── recipe_variant_id (FK) [for SPONGE, FILLING, FROSTING]
├── quantity (DECIMAL, mainly for decoration/packaging count)
├── notes

OrderIngredientUsage
├── id (PK)
├── order_id (FK)
├── ingredient_id (FK)
├── estimated_quantity (DECIMAL)
├── estimated_cost (DECIMAL)
├── actual_quantity (DECIMAL, nullable)
├── actual_cost (DECIMAL, nullable)
├── unit_used (ingredient unit at time of order)

OrderSupplyUsage
├── id (PK)
├── order_id (FK)
├── supply_id (FK)
├── estimated_quantity (DECIMAL)
├── estimated_cost (DECIMAL)
├── actual_quantity (DECIMAL, nullable)
├── actual_cost (DECIMAL, nullable)

LaborEntry
├── id (PK)
├── order_id (FK)
├── activity (ENUM: PREP, BAKING, FILLING, FROSTING, DECORATION, CLEANUP)
├── estimated_minutes (INT)
├── actual_minutes (INT, nullable)
├── hourly_rate (DECIMAL, at time of recording)
├── notes
├── created_at, updated_at

├─────────────────────────────────────────────────────────────────────────┤
│                        COSTS & OPERATING EXPENSES                       │
├─────────────────────────────────────────────────────────────────────────┤

OperatingCostCategory
├── id (PK)
├── name (e.g., "Electricity", "Gas", "Packaging", "Delivery")
├── description
├── cost_type (ENUM: FIXED_PER_ORDER, USAGE_BASED)
├── default_amount (DECIMAL, if fixed)
├── active
├── created_at, updated_at

OrderOperatingCost
├── id (PK)
├── order_id (FK)
├── operating_cost_category_id (FK)
├── estimated_amount (DECIMAL)
├── actual_amount (DECIMAL, nullable)
├── notes

OrderCostSummary (denormalized for quick access)
├── id (PK)
├── order_id (FK, UNIQUE)
├── ingredient_cost_estimated (DECIMAL)
├── ingredient_cost_actual (DECIMAL, nullable)
├── supply_cost_estimated (DECIMAL)
├── supply_cost_actual (DECIMAL, nullable)
├── labor_cost_estimated (DECIMAL)
├── labor_cost_actual (DECIMAL, nullable)
├── operating_cost_estimated (DECIMAL)
├── operating_cost_actual (DECIMAL, nullable)
├── total_cost_estimated (DECIMAL)
├── total_cost_actual (DECIMAL, nullable)
├── updated_at

Payment
├── id (PK)
├── order_id (FK)
├── amount (DECIMAL)
├── payment_date
├── payment_method (e.g., "CASH", "CARD", "BANK_TRANSFER")
├── notes
├── created_at
```

---

## 2. Table Definitions with SQLAlchemy Pseudo-Code

### 2.1 Users Table

```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hourly_rate = Column(Numeric(10, 2), default=20.00, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### 2.2 Ingredients Table

```python
class Ingredient(Base):
    __tablename__ = "ingredients"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    category = Column(String(100))  # "Dry", "Liquid", "Perishable", etc.
    base_unit = Column(String(20), nullable=False)  # "g", "ml", "cup", etc.
    current_cost_per_unit = Column(Numeric(10, 4), nullable=False)  # per base_unit
    current_quantity = Column(Numeric(12, 2), default=0)  # in base_unit
    min_threshold = Column(Numeric(12, 2), default=0)
    supplier = Column(String(255))
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transactions = relationship("InventoryTransaction", back_populates="ingredient")
    recipe_ingredients = relationship("RecipeIngredient", back_populates="ingredient")
    units = relationship("IngredientUnit", back_populates="ingredient")
    order_usages = relationship("OrderIngredientUsage", back_populates="ingredient")
```

### 2.3 InventoryTransaction Table

```python
class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"
    
    id = Column(Integer, primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)  # PURCHASE, CONSUMPTION, ADJUSTMENT, WASTE, RETURN
    quantity_change = Column(Numeric(12, 2), nullable=False)  # signed (positive/negative)
    transaction_date = Column(Date, nullable=False)
    purchase_price_per_unit = Column(Numeric(10, 4))  # only for PURCHASE
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    ingredient = relationship("Ingredient", back_populates="transactions")
```

### 2.4 Recipes & Recipe Variants

```python
class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100))  # "Sponge", "Filling", "Frosting", "Decoration"
    description = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    variants = relationship("RecipeVariant", back_populates="recipe", cascade="all, delete-orphan")

class RecipeVariant(Base):
    __tablename__ = "recipe_variants"
    
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    variant_name = Column(String(255), nullable=False)  # "6-inch 2-layer"
    base_yield = Column(Numeric(8, 2), nullable=False)  # quantity produced
    yield_unit = Column(String(50), nullable=False)  # "cake", "batch", "dozen"
    description = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    recipe = relationship("Recipe", back_populates="variants")
    ingredients = relationship("RecipeIngredient", back_populates="recipe_variant", cascade="all, delete-orphan")
    order_components = relationship("OrderComponent", foreign_keys="OrderComponent.recipe_variant_id")

class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    
    id = Column(Integer, primary_key=True)
    recipe_variant_id = Column(Integer, ForeignKey("recipe_variants.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    quantity_required = Column(Numeric(12, 2), nullable=False)
    unit = Column(String(50), nullable=False)  # ingredient-specific unit
    
    recipe_variant = relationship("RecipeVariant", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="recipe_ingredients")
```

### 2.5 Customers & Orders

```python
class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    phone = Column(String(20))
    address = Column(Text)
    notes = Column(Text)  # dietary restrictions, preferences
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    orders = relationship("Order", back_populates="customer")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    order_date = Column(Date, nullable=False)
    delivery_date = Column(Date)
    status = Column(Enum(OrderStatus), default=OrderStatus.QUOTE, nullable=False)
    selling_price = Column(Numeric(10, 2), nullable=False)
    discount_amount = Column(Numeric(10, 2), default=0)
    tax_rate = Column(Numeric(5, 2), default=0)  # percentage
    tax_amount = Column(Numeric(10, 2), default=0)
    deposit_amount = Column(Numeric(10, 2), default=0)
    amount_paid = Column(Numeric(10, 2), default=0)
    estimated_total_cost = Column(Numeric(10, 2))  # calculated
    actual_total_cost = Column(Numeric(10, 2))  # updated on completion
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    customer = relationship("Customer", back_populates="orders")
    components = relationship("OrderComponent", back_populates="order", cascade="all, delete-orphan")
    ingredient_usages = relationship("OrderIngredientUsage", back_populates="order", cascade="all, delete-orphan")
    supply_usages = relationship("OrderSupplyUsage", back_populates="order", cascade="all, delete-orphan")
    labor_entries = relationship("LaborEntry", back_populates="order", cascade="all, delete-orphan")
    operating_costs = relationship("OrderOperatingCost", back_populates="order", cascade="all, delete-orphan")
    cost_summary = relationship("OrderCostSummary", back_populates="order", uselist=False, cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan")
```

### 2.6 Order Components

```python
class OrderComponent(Base):
    __tablename__ = "order_components"
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    component_type = Column(Enum(ComponentType), nullable=False)  # SPONGE, FILLING, FROSTING, DECORATION, PACKAGING
    recipe_variant_id = Column(Integer, ForeignKey("recipe_variants.id"))  # for SPONGE, FILLING, FROSTING
    supply_id = Column(Integer, ForeignKey("cake_supplies.id"))  # for DECORATION, PACKAGING
    quantity = Column(Numeric(8, 2), default=1)  # for supplies
    notes = Column(Text)
    
    order = relationship("Order", back_populates="components")
    recipe_variant = relationship("RecipeVariant", foreign_keys=[recipe_variant_id])
    supply = relationship("CakeSupply", foreign_keys=[supply_id])
```

### 2.7 Labor Entries

```python
class LaborEntry(Base):
    __tablename__ = "labor_entries"
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    activity = Column(Enum(Activity), nullable=False)  # PREP, BAKING, FILLING, FROSTING, DECORATION, CLEANUP
    estimated_minutes = Column(Integer)
    actual_minutes = Column(Integer)  # nullable until completed
    hourly_rate = Column(Numeric(10, 2), nullable=False)  # rate at time of recording
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    order = relationship("Order", back_populates="labor_entries")
```

### 2.8 Operating Costs

```python
class OperatingCostCategory(Base):
    __tablename__ = "operating_cost_categories"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    cost_type = Column(Enum(CostType), nullable=False)  # FIXED_PER_ORDER, USAGE_BASED
    default_amount = Column(Numeric(10, 2))  # for FIXED_PER_ORDER
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class OrderOperatingCost(Base):
    __tablename__ = "order_operating_costs"
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    operating_cost_category_id = Column(Integer, ForeignKey("operating_cost_categories.id"), nullable=False)
    estimated_amount = Column(Numeric(10, 2), nullable=False)
    actual_amount = Column(Numeric(10, 2))  # nullable until completed
    notes = Column(Text)
    
    order = relationship("Order", back_populates="operating_costs")
    category = relationship("OperatingCostCategory")
```

### 2.9 Cost Summary (Denormalized)

```python
class OrderCostSummary(Base):
    __tablename__ = "order_cost_summary"
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    ingredient_cost_estimated = Column(Numeric(10, 2), default=0)
    ingredient_cost_actual = Column(Numeric(10, 2))
    supply_cost_estimated = Column(Numeric(10, 2), default=0)
    supply_cost_actual = Column(Numeric(10, 2))
    labor_cost_estimated = Column(Numeric(10, 2), default=0)
    labor_cost_actual = Column(Numeric(10, 2))
    operating_cost_estimated = Column(Numeric(10, 2), default=0)
    operating_cost_actual = Column(Numeric(10, 2))
    total_cost_estimated = Column(Numeric(10, 2), default=0)
    total_cost_actual = Column(Numeric(10, 2))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    order = relationship("Order", back_populates="cost_summary")
```

---

## 3. Enums

```python
class TransactionType(Enum):
    PURCHASE = "PURCHASE"
    CONSUMPTION = "CONSUMPTION"
    ADJUSTMENT = "ADJUSTMENT"
    WASTE = "WASTE"
    RETURN = "RETURN"

class OrderStatus(Enum):
    QUOTE = "QUOTE"
    CONFIRMED = "CONFIRMED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class ComponentType(Enum):
    SPONGE = "SPONGE"
    FILLING = "FILLING"
    FROSTING = "FROSTING"
    DECORATION = "DECORATION"
    PACKAGING = "PACKAGING"

class Activity(Enum):
    PREP = "PREP"
    BAKING = "BAKING"
    FILLING = "FILLING"
    FROSTING = "FROSTING"
    DECORATION = "DECORATION"
    CLEANUP = "CLEANUP"

class CostType(Enum):
    FIXED_PER_ORDER = "FIXED_PER_ORDER"
    USAGE_BASED = "USAGE_BASED"
```

---

## 4. Indexes

```sql
-- Frequently queried columns
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_orders_delivery_date ON orders(delivery_date);

CREATE INDEX idx_inventory_transactions_ingredient_id ON inventory_transactions(ingredient_id);
CREATE INDEX idx_inventory_transactions_date ON inventory_transactions(transaction_date);

CREATE INDEX idx_recipe_ingredients_recipe_variant_id ON recipe_ingredients(recipe_variant_id);
CREATE INDEX idx_recipe_ingredients_ingredient_id ON recipe_ingredients(ingredient_id);

CREATE INDEX idx_order_components_order_id ON order_components(order_id);
CREATE INDEX idx_order_ingredient_usage_order_id ON order_ingredient_usage(order_id);
CREATE INDEX idx_order_supply_usage_order_id ON order_supply_usage(order_id);

CREATE INDEX idx_labor_entries_order_id ON labor_entries(order_id);
CREATE INDEX idx_order_operating_costs_order_id ON order_operating_costs(order_id);

-- Unique constraints
CREATE UNIQUE INDEX idx_order_cost_summary_order_id ON order_cost_summary(order_id);
```

---

## 5. Migration Strategy

Use Alembic for all schema changes:

```bash
# Initial migration
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head

# Future changes
alembic revision --autogenerate -m "Add new column"
alembic upgrade head
```

No manual table creation. All changes tracked in version control.

