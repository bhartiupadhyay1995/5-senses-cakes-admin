# Phase 1: Requirements and Architecture
## 5 Senses Cakes — Business Management Application

**Date**: September 2026  
**Status**: Requirements finalized and clarified  
**Next Phase**: Phase 2 — Database Design and Implementation

---

## 1. Clarified Requirements (User Input)

### 1.1 Authentication
- **Single-user application** — built for the business owner only
- Architecture should be **auth-ready** (simple to add multi-user support later if needed)
- No complex role-based access control initially

### 1.2 Ingredient Units
- Support **multiple measurement units** for the same ingredient
- Example: Flour can be stored/purchased in both **grams** and **cups**
- System should handle unit conversions (kg ↔ g, L ↔ ml, dozen ↔ individual)
- Costs are normalized to a base unit for calculations

### 1.3 Ingredient Pricing
- Use **current price in database** for all cost calculations
- Do NOT track historical price changes per purchase
- Simpler model: when an ingredient is updated to a new price, that price is used for all calculations going forward
- Historical purchase prices are still recorded for audit purposes

### 1.4 Orders and Customers
- Track **customer details** (name, contact info)
- Track order dates and delivery dates
- Identify **recurring customers** (by count/frequency)
- Analyze profitability per customer
- Support deposit tracking and payment status

### 1.5 Analytics Priority
- **All proposed analytics are important**
- Dashboard should show: today, this week, this month
- Drill-down capability to individual orders and ingredients
- Support date filtering and customizable analytics

---

## 2. Functional Requirements

### 2.1 Core Modules

#### Inventory Management
- Track **ingredients** (food items) and **supplies** (non-food items)
- Each item has: name, category, unit, purchase quantity, purchase price, cost per unit, current quantity, minimum quantity
- **Inventory transactions** (PURCHASE, CONSUMPTION, ADJUSTMENT, WASTE, RETURN)
- Maintain full transaction history (never mutate inventory count directly)
- Support multiple units per ingredient with automatic conversions

#### Recipes
- Store recipes with: name, category, description, version, yield, yield unit
- Each recipe contains ingredient quantities
- Support **recipe variants** (e.g., 6-inch 2-layer vs. 8-inch 3-layer)
- Auto-calculate recipe cost based on current ingredient prices
- Allow recipe scaling

#### Orders
- Complete order lifecycle: QUOTE → CONFIRMED → IN_PROGRESS → COMPLETED/CANCELLED
- Order composition:
  - Cake size, layers
  - Sponge (recipe variant)
  - Filling (recipe variant)
  - Frosting (recipe variant)
  - Design and decorations
  - Packaging items
- Customer information and contact details
- Order dates (taken, delivery/pickup)
- Payment status and deposits

#### Cost Tracking
- **Estimated costs** (calculated when order created)
  - Ingredient cost (from recipes)
  - Decoration/supply cost
  - Packaging cost
  - Labor estimate
  - Operating costs
- **Actual costs** (recorded when order completed)
  - Actual ingredient/supply usage
  - Actual labor time
  - Actual operating costs
- Clear distinction between estimated and actual

#### Labor Tracking
- Default labor time per cake type/design
- Actual labor time entry per order
- Configurable **hourly labor rate** (editable globally and per-order)
- Break down labor by activity (prep, baking, filling, frosting, decoration, cleanup)

#### Operating Costs
- Configurable cost categories: electricity, gas, cleaning supplies, packaging, delivery, payment fees, etc.
- Fixed-per-order model initially
- Architecture allows for usage-based costs in future

#### Profitability Analysis
- **Revenue**: selling price (minus discount, plus tax if applicable)
- **Direct material cost**: ingredients + decorations + packaging
- **Direct labor cost**: actual hours × hourly rate
- **Gross profit**: revenue − direct material − direct labor
- **Operating profit**: revenue − all tracked costs
- Clear labeling of what's included in each profit metric

### 2.2 Key Calculations (Business Logic)

#### Cost Calculations
```
Ingredient Cost = Sum of (quantity used × current unit cost for each ingredient)
Supply Cost = Sum of (quantity × current unit cost for supplies)
Labor Cost = total hours worked × hourly labor rate
Operating Cost = Sum of configured operating costs
Total Cost = Ingredient + Supply + Labor + Operating costs
```

#### Revenue & Profit
```
Revenue = selling price (considering discounts, deposits, taxes)
Gross Profit = Revenue − Ingredient Cost − Supply Cost − Labor Cost
Operating Profit = Revenue − Total Cost
Profit Margin = (Gross Profit / Revenue) × 100
```

#### Inventory
```
Current Inventory = Sum of all transactions (PURCHASE - CONSUMPTION - WASTE ± ADJUSTMENTS)
Min/Low Stock Alert = Current Inventory < Minimum Threshold
```

### 2.3 Auditability Requirements
- Click through any cost line to see the calculation breakdown
- Example: "Flour 250g × $0.002/g = $0.50"
- Show labor: "4.2 hours × $20/hour = $84"
- Maintain full transaction history for all inventory movements
- Purchase history is auditable

---

## 3. Non-Functional Requirements

### 3.1 Technology Stack
- **Frontend**: React 18+, TypeScript, Vite, Tailwind CSS, shadcn/ui, React Router, TanStack Query
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, Alembic, Pydantic
- **Database**: PostgreSQL 14+
- **Testing**: Pytest (backend), Playwright (E2E)
- **Deployment**: Docker Compose
- **Development**: Git/GitHub, GitHub Copilot

### 3.2 Responsiveness
- Desktop, laptop, tablet, mobile browser support
- Touch-friendly UI
- Clean, modern dashboard appropriate for a bakery
- Simplicity over visual complexity

### 3.3 Data Integrity
- Use `NUMERIC` / `DECIMAL` types for all currency values
- No floating-point arithmetic for financial calculations
- Use Decimal-compatible logic in backend
- Proper constraint enforcement at database level

### 3.4 Performance Considerations
- Single-user application (optimization can be minimal initially)
- Real-time dashboard updates not required
- Batch operations for inventory adjustments

### 3.5 Deployment
- **Local deployment only** via Docker Compose
- Single command: `docker compose up`
- No manual installation of: PostgreSQL, Python, Node.js, Redis, other infrastructure
- Environment configuration via `.env` file
- Git + Docker Desktop is all that's needed

---

## 4. Domain Model (ERD Conceptual)

### 4.1 Core Entities

#### User
- Single user application
- Fields: id, name, email, hourly_rate, created_at, updated_at
- Future: support for multi-user with roles

#### Ingredient
- name, category, active_status
- current_unit (base unit for calculations)
- current_cost_per_unit
- current_inventory_quantity
- min_inventory_threshold
- supplier, notes

#### InventoryTransaction
- ingredient_id (FK)
- transaction_type (PURCHASE, CONSUMPTION, ADJUSTMENT, WASTE, RETURN)
- quantity_change
- transaction_date
- purchase_price_per_unit (if PURCHASE)
- notes, created_at

#### Recipe
- name, category, description, yield, yield_unit, version, active
- created_at, updated_at

#### RecipeVariant
- recipe_id (FK)
- variant_name (e.g., "6-inch 2-layer")
- base_yield, yield_unit
- description

#### RecipeIngredient
- recipe_variant_id (FK)
- ingredient_id (FK)
- quantity_required
- unit (may differ from ingredient base unit)

#### CakeSupply
- Similar structure to Ingredient (non-food items)
- toppers, boards, boxes, candles, fondant, etc.

#### Customer
- name, contact_info (email, phone)
- created_at, updated_at
- notes (dietary preferences, special requests, etc.)

#### Order
- customer_id (FK)
- order_date, delivery_date
- status (QUOTE, CONFIRMED, IN_PROGRESS, COMPLETED, CANCELLED)
- selling_price, discount, tax_rate
- deposit_amount, amount_paid, amount_remaining
- notes

#### OrderComponent
- order_id (FK)
- component_type (SPONGE, FILLING, FROSTING, DECORATION, PACKAGING)
- recipe_variant_id or supply_id (polymorphic-like)
- quantity

#### OrderIngredientUsage
- order_id (FK)
- ingredient_id (FK)
- estimated_quantity, estimated_cost
- actual_quantity, actual_cost (nullable until order completed)

#### OrderCost
- order_id (FK)
- cost_category (INGREDIENT, SUPPLY, LABOR, OPERATING, DECORATION)
- estimated_amount
- actual_amount (nullable until completed)
- cost_details_json (for auditability)

#### LaborEntry
- order_id (FK)
- activity (PREP, BAKING, FILLING, FROSTING, DECORATION, CLEANUP)
- estimated_minutes
- actual_minutes (nullable)
- hourly_rate (at time of recording)

#### OperatingCostCategory
- name, description, cost_type (FIXED_PER_ORDER or USAGE_BASED)
- default_amount
- active

#### OrderOperatingCost
- order_id (FK)
- operating_cost_category_id (FK)
- estimated_amount, actual_amount

---

## 5. API Architecture

### 5.1 API Endpoints (RESTful)

#### Inventory
- `GET /api/ingredients` — list all
- `POST /api/ingredients` — create
- `GET /api/ingredients/{id}` — get details
- `PUT /api/ingredients/{id}` — update
- `GET /api/ingredients/{id}/transactions` — transaction history
- `POST /api/inventory-transactions` — record transaction (purchase, consumption, etc.)

#### Recipes
- `GET /api/recipes` — list all
- `POST /api/recipes` — create
- `GET /api/recipes/{id}` — get with variants and ingredients
- `POST /api/recipes/{id}/variants` — add variant
- `GET /api/recipes/{id}/cost` — calculate recipe cost

#### Orders
- `GET /api/orders` — list with filtering
- `POST /api/orders` — create
- `GET /api/orders/{id}` — get full order details
- `PUT /api/orders/{id}` — update order
- `PUT /api/orders/{id}/status` — change status
- `POST /api/orders/{id}/labor` — record labor time
- `POST /api/orders/{id}/usage` — record actual ingredient usage
- `GET /api/orders/{id}/costs` — get cost breakdown
- `GET /api/orders/{id}/profitability` — get profit analysis

#### Analytics
- `GET /api/analytics/dashboard?period=today|week|month` — dashboard metrics
- `GET /api/analytics/revenue?start_date=X&end_date=Y` — revenue by period
- `GET /api/analytics/profit?filters=...` — profit analysis
- `GET /api/analytics/orders?status=COMPLETED&filters=...` — order analysis
- `GET /api/analytics/inventory-usage` — ingredient usage trends
- `GET /api/analytics/customers` — customer analytics (recurring, profit per customer)

#### Pricing Calculator
- `POST /api/pricing-calculator/estimate` — calculate estimated costs and suggested price

#### Customer
- `GET /api/customers` — list all
- `POST /api/customers` — create
- `GET /api/customers/{id}` — get details
- `GET /api/customers/{id}/orders` — customer's order history

---

## 6. Frontend Architecture

### 6.1 Page Structure

#### Dashboard
- Today's metrics card
- This week's summary
- This month's summary
- Chart: revenue/profit trends
- Low inventory alerts
- Recent orders

#### Inventory Section
- Ingredients list (with current cost, quantity, minimum threshold)
- Supplies list
- Inventory transactions view
- Add/edit ingredient form
- Add purchase form

#### Recipes Section
- Recipes list
- Create/edit recipe
- Manage variants
- View recipe cost
- Recipe scaling calculator

#### Orders Section
- Orders list (filterable by status, customer, date)
- Create new order
- Order details page
- Cost and profitability breakdown
- Edit order status
- Record labor time
- Record actual usage

#### Analytics Section
- Date range selector (today, week, month, custom)
- Revenue/cost/profit charts
- Order analysis (avg profit, most profitable)
- Ingredient usage trends
- Customer analysis (recurring customers, profit per customer)
- Export data (CSV)

#### Settings
- Hourly labor rate
- Operating cost categories
- User preferences

### 6.2 Component Architecture
- Reusable form components
- Data table component (sortable, filterable, pageable)
- Chart components (Recharts)
- Modal dialogs for create/edit
- Cost breakdown detail views

---

## 7. Database Schema Approach

### 7.1 Key Design Decisions
- Use Alembic for all schema migrations
- Soft deletes where appropriate (active/inactive flags)
- Audit fields: created_at, updated_at on key tables
- Foreign keys with CASCADE or RESTRICT as appropriate
- Indexes on frequently filtered columns (order_date, customer_id, status)
- Decimal type for all monetary values

### 7.2 Tables (Preliminary)
```
users
ingredients
ingredient_units (for multi-unit support)
inventory_transactions
cake_supplies
recipes
recipe_variants
recipe_ingredients
customers
orders
order_components
order_ingredient_usage
order_supply_usage
labor_entries
operating_cost_categories
order_operating_costs
order_costs (summary table for quick access)
payments
```

---

## 8. Testing Strategy

### 8.1 Backend Testing (Pytest)
- Unit tests for cost calculations
- Unit tests for inventory calculations
- Unit tests for profit calculations
- Integration tests for API endpoints
- Database tests (with test fixtures)
- Edge cases: negative inventory, cost overrides, etc.

### 8.2 Frontend Testing (Playwright)
- Critical workflows:
  - Create ingredient
  - Create recipe
  - Create order
  - Complete order with actual usage
  - View profitability
  - View analytics

### 8.3 Financial Accuracy
- Every calculation path has unit tests
- Decimal arithmetic verified
- Audit trail can be traced for any calculation

---

## 9. Assumptions & Constraints

### 9.1 Assumptions
1. Single-user operation (owner only)
2. Current ingredient pricing (no historical tracking)
3. Ingredient prices are relatively stable
4. Labor rate is globally configurable
5. Operating costs are simple per-order or globally configured
6. Desktop/mobile browser access sufficient (no native apps)
7. Local deployment only
8. Small business scale (< 50 orders/month initially)

### 9.2 Constraints
- No floating-point currency arithmetic
- All costs must be traceable/auditable
- No complex role-based access control in phase 1
- No payment gateway integration
- No automatic inventory reordering

---

## 10. Phase 1 Deliverables

By the end of Phase 1, we will have:

1. **This document** — finalized requirements and architecture
2. **Database schema** — ERD and SQL migrations ready
3. **API specification** — detailed endpoint documentation
4. **Frontend wireframes** — key page layouts
5. **Cost calculation rules** — documented formulas
6. **Assumption log** — any ambiguities resolved

---

## 11. Next Steps

**Phase 2**: Database design and implementation
- Finalize ERD
- Create PostgreSQL schema with Alembic
- Create SQLAlchemy models
- Create test fixtures

