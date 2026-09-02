# 5 Senses Cakes - Backend

## Database Models - Phase 2 Implementation ✓

All database models have been implemented according to the design specification in `docs/DATABASE_SCHEMA.md`.

### Implemented Entities

#### Core Inventory
- **User** - Single user for business owner (name, email, hourly_rate)
- **Ingredient** - Food items used in recipes
- **IngredientUnit** - Support for multiple units per ingredient
- **InventoryTransaction** - Track ingredient movements (purchase, consumption, adjustment, waste, return)
- **CakeSupply** - Non-food supplies (boxes, boards, toppers, etc.)
- **SupplyTransaction** - Track supply movements

#### Recipes
- **Recipe** - Base recipe entity (sponge, filling, frosting, decoration)
- **RecipeVariant** - Specific recipe configurations (sizes, layers, etc.)
- **RecipeIngredient** - Ingredients required in a recipe variant

#### Customers & Orders
- **Customer** - Customer information and contact details
- **Order** - Main order entity with pricing, payment, and cost tracking
- **OrderComponent** - Order breakdown by component type
- **OrderIngredientUsage** - Ingredient usage tracking (estimated and actual)
- **OrderSupplyUsage** - Supply usage tracking (estimated and actual)

#### Labor & Costs
- **LaborEntry** - Track labor activities (prep, baking, filling, frosting, decoration, cleanup)
- **OperatingCostCategory** - Categories for operating expenses
- **OrderOperatingCost** - Operating costs per order
- **OrderCostSummary** - Denormalized cost summary for quick access

### File Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── database.py            # Database connection and session management
│   └── models/
│       ├── __init__.py        # Model exports
│       ├── base.py            # Base model with common fields
│       ├── user.py
│       ├── customer.py
│       ├── ingredient.py      # Ingredients and inventory tracking
│       ├── recipe.py          # Recipes and variants
│       ├── order.py           # Orders and components
│       ├── labor.py           # Labor tracking
│       ├── operating_cost.py  # Operating costs
│       └── enums.py           # Enum definitions
├── migrations/
│   ├── env.py                 # Alembic environment
│   ├── script.py.mako         # Migration template
│   └── versions/
│       └── 001_initial_schema.py  # Initial schema migration
├── main.py                    # FastAPI application entry point
├── init_db.py                 # Database initialization script
├── alembic.ini                # Alembic configuration
├── run_migrations.sh          # Migration runner script
├── .env.example               # Environment variables template
├── requirements.txt
├── Dockerfile
└── README.md
```

### Setup & Usage

#### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your PostgreSQL configuration
```

#### 3. Initialize Database
Option A - Using Alembic migrations (recommended):
```bash
chmod +x run_migrations.sh
./run_migrations.sh
```

Option B - Direct initialization:
```bash
python init_db.py
```

#### 4. Run the Application
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Database Enums

The application uses PostgreSQL enums for type safety:

- **TransactionType**: PURCHASE, CONSUMPTION, ADJUSTMENT, WASTE, RETURN
- **OrderStatus**: QUOTE, CONFIRMED, IN_PROGRESS, COMPLETED, CANCELLED
- **ComponentType**: SPONGE, FILLING, FROSTING, DECORATION, PACKAGING
- **Activity**: PREP, BAKING, FILLING, FROSTING, DECORATION, CLEANUP
- **CostType**: FIXED_PER_ORDER, USAGE_BASED
- **PaymentMethod**: CASH, CARD

### Key Design Decisions

1. **Denormalization**: OrderCostSummary table provides quick access to cost data without complex calculations
2. **Audit Trail**: All tables have created_at and updated_at timestamps
3. **Flexible Inventory**: Support for multiple units per ingredient (e.g., grams and cups)
4. **Cost Tracking**: Separate estimated and actual costs for all items
5. **Foreign Keys**: All relationships include proper foreign key constraints

### Next Steps

- Phase 3: Implement REST API endpoints
- Add authentication and authorization
- Create request/response schemas
- Implement business logic for cost calculations
- Add validation and error handling
