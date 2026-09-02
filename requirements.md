# 5 Senses Cakes — Personalized Cake Business Management Application

## 1. Project Overview

I own a small home-based cake business called **5 Senses Cakes**.

I want to build a personalized web application to manage:

1. Ingredients and inventory
2. Non-food cake supplies
3. Ingredient/supply costs
4. Cake recipes
5. Cake orders
6. Estimated ingredient and supply costs
7. Actual ingredient and supply usage
8. Labor/time spent on each order
9. Other operating costs such as electricity and packaging
10. Revenue
11. Gross profit
12. Profitability by order
13. Daily, weekly, and monthly business analysis

The application should be designed specifically for a small made-to-order cake business rather than a generic enterprise inventory system.

The application must be easy to use through a web-based UI. I should NOT need to manually edit database tables or SQL queries for normal business operations.

---

# 2. Development Philosophy

Use a **spec-driven and incremental development approach**.

Do NOT attempt to build the entire application in one step.

Development should happen in the following phases:

### Phase 1 — Requirements and architecture

Define:

* Functional requirements
* Non-functional requirements
* User workflows
* Domain model
* Database schema
* API architecture
* Frontend architecture
* Cost calculation rules
* Profit calculation rules

Before implementation, identify ambiguities and make reasonable assumptions.

Do not introduce unnecessary complexity.

---

### Phase 2 — Database

Design and implement the PostgreSQL database schema.

Create proper:

* Primary keys
* Foreign keys
* Unique constraints
* Indexes
* Created/updated timestamps
* Soft-delete strategy where appropriate
* Audit fields where useful

Use SQLAlchemy models and Alembic migrations.

Database changes must always be made through migrations.

Never require the user to manually create tables.

---

### Phase 3 — Backend API

Build a REST API using Python and FastAPI.

The backend should contain:

* Authentication-ready architecture
* Business logic
* Validation
* Database access
* Cost calculations
* Inventory calculations
* Profit calculations

Business calculations should be implemented in the backend rather than duplicated in the frontend.

---

### Phase 4 — Frontend

Build a responsive React + TypeScript UI.

The application should be usable on:

* Desktop
* Laptop
* Tablet
* Mobile browser

Use a clean, modern dashboard appropriate for a small bakery.

Prioritize simplicity over visual complexity.

---

### Phase 5 — Testing

Add automated tests for:

* Database operations
* Recipe calculations
* Inventory calculations
* Cost calculations
* Profit calculations
* API endpoints
* Important UI workflows

Critical financial calculations must have unit tests.

---

### Phase 6 — Local deployment

The application must run locally using Docker Compose.

A new computer should require only:

1. Git
2. Docker Desktop
3. Repository clone
4. Environment configuration

The user should NOT need to manually install:

* PostgreSQL
* Python
* Node.js
* npm
* Redis
* Other infrastructure

unless absolutely necessary.

The goal is that the entire application can be started with:

```bash
docker compose up
```

or an equivalent single command.

---

# 3. Recommended Technology Stack

Use the following stack unless there is a strong technical reason to change it.

## Frontend

* React
* TypeScript
* Vite
* Tailwind CSS
* shadcn/ui or another lightweight accessible component library
* React Router
* React Query / TanStack Query
* Recharts for analytics

## Backend

* Python
* FastAPI
* SQLAlchemy
* Alembic
* Pydantic

## Database

* PostgreSQL

Use PostgreSQL as the primary source of truth.

## Development

* Git
* GitHub
* GitHub Copilot
* Docker
* Docker Compose

## Testing

Backend:

* Pytest

Frontend/end-to-end:

* Playwright

---

# 4. Core Domain Model

The application should contain the following major entities.

## 4.1 Ingredients

Examples:

* All-purpose flour
* Granulated sugar
* Icing sugar
* Eggs
* Butter
* Oil
* Milk
* Heavy cream
* Chocolate
* Cocoa powder
* Vanilla
* Mango pulp
* Strawberries
* Raspberries

Each ingredient should contain:

* ID
* Name
* Category
* Unit of measurement
* Purchase quantity
* Purchase unit
* Purchase price
* Cost per base unit
* Current inventory quantity
* Minimum inventory threshold
* Supplier (optional)
* Active/inactive status
* Notes

The system should normalize costs to a base unit.

Example:

If I purchase:

10 kg sugar for $15

the system should calculate:

$1.50/kg

and internally be able to calculate:

100 g sugar = $0.15

The system must support unit conversions where practical.

For example:

* kg → g
* L → ml
* dozen → individual eggs

Avoid unsafe or ambiguous automatic conversions.

---

# 5. Non-Food Inventory / Cake Supplies

Inventory should NOT be limited to ingredients.

I also need to manage cake supplies such as:

* Cake boxes
* Cake boards
* Fondant
* Toppers
* Candles
* Dowels
* Cake supports
* Edible images
* Food coloring
* Piping bags
* Disposable items
* Packaging material
* Ribbon
* Stickers
* Other decorating supplies

These should use the same inventory framework where practical.

Each inventory item should have:

* Name
* Category
* Unit
* Purchase quantity
* Purchase price
* Cost per unit
* Current quantity
* Minimum quantity
* Supplier
* Notes

---

# 6. Inventory Transactions

Do NOT simply store one mutable inventory number.

Maintain an inventory transaction/history model.

Possible transaction types:

* PURCHASE
* CONSUMPTION
* ADJUSTMENT
* WASTE
* RETURN

Example:

I purchase:

10 kg flour

Inventory:

+10 kg

I complete a cake using:

250 g flour

Inventory:

-250 g

The application should maintain the transaction history.

The UI should allow me to view:

* Current inventory
* Inventory movement
* Purchase history
* Consumption history
* Waste
* Adjustments

---

# 7. Recipes

Recipes are a core part of the application.

Examples:

* Vanilla Sponge
* Chocolate Sponge
* Red Velvet Sponge
* Mango Filling
* Strawberry Filling
* Raspberry Filling
* Nutella Filling
* Chocolate Ganache
* Whipped Cream Frosting

A recipe should contain:

* Recipe name
* Recipe category
* Description
* Ingredients
* Quantity of each ingredient
* Base yield
* Yield unit
* Recipe version
* Notes

Example:

## Vanilla Sponge — 6 inch / 2 layer

Flour: 250 g
Sugar: 180 g
Eggs: 3
Oil: 80 ml
Milk: 100 ml
Vanilla: 5 ml

The system should calculate the recipe's estimated cost automatically using the current ingredient costs.

---

# 8. Recipe Scaling

Recipes must support scaling.

For example, if a recipe is defined for:

6-inch / 2-layer cake

the system should allow it to be used for:

* 4 inch
* 6 inch
* 8 inch
* 9 inch
* Different number of layers

However, do NOT assume that scaling is always a simple mathematical relationship.

The system should support explicit recipe variants.

For example:

Vanilla Sponge:

* 6 inch / 2 layer
* 6 inch / 3 layer
* 8 inch / 2 layer
* 8 inch / 4 layer

Each variant may have its own ingredient quantities.

This is preferable to automatically assuming that an 8-inch cake requires exactly X times the ingredients.

---

# 9. Cake Products / Components

A cake order should be composed of multiple components.

For example:

## Cake Order

6-inch
2 layers

Sponge:
Vanilla

Filling:
Mango

Frosting:
Whipped Cream

Design:
Custom floral design

Decorations:
Edible topper

Packaging:
6-inch cake box
6-inch cake board

The system should calculate the estimated cost of all components.

---

# 10. Orders

Create an Order module.

Each order should contain:

* Order ID
* Customer name
* Customer contact information
* Order date
* Pickup/delivery date
* Status
* Cake size
* Number of layers
* Sponge
* Filling
* Frosting
* Design
* Toppers
* Other decorations
* Packaging
* Selling price
* Deposit/payment information
* Notes

Order status could include:

* QUOTE
* CONFIRMED
* IN_PROGRESS
* COMPLETED
* CANCELLED

---

# 11. Estimated Cost

When an order is created, calculate the estimated cost automatically.

Estimated cost should include:

### Ingredient cost

Based on:

Recipe quantity × current ingredient unit cost

### Decoration/supply cost

Based on selected:

* toppers
* fondant
* boards
* boxes
* candles
* edible images
* other supplies

### Packaging cost

Based on selected packaging items.

### Labor estimate

Based on default labor time for the selected cake/design.

### Other operating costs

Examples:

* Electricity
* Gas
* Cleaning supplies
* Disposable supplies

The system should clearly distinguish estimated and actual costs.

---

# 12. Actual Usage

This is a critical requirement.

The recipe may say:

Mango = 250 g

But in reality I may use:

320 g

The application must allow me to record actual usage.

Therefore each completed order should have:

### Estimated usage

and

### Actual usage

Actual usage should override the estimated usage when entered.

Example:

Estimated ingredient cost:

$20

Actual ingredient cost:

$23.50

The application should show the difference.

---

# 13. Labor / Time Tracking

Each order should have labor tracking.

For example:

Preparation: 30 minutes
Baking: 45 minutes
Filling: 30 minutes
Frosting: 45 minutes
Decoration: 90 minutes
Cleanup: 20 minutes

Total:

4 hours 20 minutes

The system should allow a default labor time.

Example:

6-inch basic cake:

2.5 hours

Custom design:

+1.5 hours

The user should be able to override the default.

The system should have a configurable:

### Labor hourly rate

Example:

$20/hour

Labor cost:

Total hours × hourly labor rate

The labor rate must be configurable globally and ideally overrideable per order.

---

# 14. Operating Costs

Create a configurable operating-cost system.

Initially support:

* Electricity
* Gas
* Cleaning supplies
* Disposable supplies
* Packaging
* Equipment usage/depreciation
* Delivery cost
* Payment processing fees
* Other miscellaneous costs

Do not over-engineer this initially.

The user should be able to add custom cost categories.

Example:

Electricity:

Estimated cost per cake = $2

or:

Electricity:

Hourly cost = $0.50

The architecture should allow both fixed-per-order and usage-based costs in the future.

---

# 15. Revenue

Each order should store:

* Selling price
* Discount
* Tax if applicable
* Deposit
* Amount paid
* Amount remaining

Revenue should be calculated from the actual selling price.

Do not confuse revenue with profit.

---

# 16. Profit Calculation

The application should clearly distinguish:

## Revenue

Selling price received/earned from the order.

## Direct material cost

Ingredients + decorations + packaging.

## Labor cost

Actual hours × labor rate.

## Other direct operating costs

Electricity, gas, payment fees, delivery, etc.

Then calculate:

### Gross Profit

Revenue − direct material cost − direct labor cost

Also provide:

### Contribution / Operating Profit

Revenue − all tracked costs.

The UI should clearly label these metrics so the user understands what is included.

Do not call a number "profit" unless the included costs are clearly defined.

---

# 17. Order Profitability View

Every completed order should have a profitability summary.

Example:

Order #1025

Revenue:
$85.00

Ingredients:
$18.40

Decorations:
$5.00

Packaging:
$3.00

Labor:
$60.00

Other costs:
$3.00

Total cost:
$89.40

Gross profit:
$-1.40

Profit margin:
-1.65%

This should immediately show whether the cake was financially worthwhile.

---

# 18. Dashboard

Create a dashboard showing:

### Today

* Orders
* Revenue
* Cost
* Profit
* Hours worked

### This Week

* Number of cakes
* Revenue
* Ingredient cost
* Labor cost
* Other costs
* Gross profit
* Average profit/order
* Average hours/order

### This Month

Same metrics.

Also show:

### Most profitable cakes

### Least profitable cakes

### Highest revenue cakes

### Most frequently used ingredients

### Low inventory items

### Inventory value

---

# 19. Analytics

Provide date filters:

* Today
* This week
* This month
* Last month
* Custom date range

Analytics should include:

Revenue
Cost
Gross profit
Profit margin
Labor hours
Average order value
Average profit/order
Ingredient cost
Packaging cost
Other costs

Allow filtering by:

* Cake size
* Cake type
* Filling
* Design
* Customer
* Order status

---

# 20. Pricing Calculator

Create a pricing calculator.

The user should be able to select:

Cake size
Layers
Sponge
Filling
Frosting
Design
Decorations
Packaging
Estimated labor

The system should calculate:

Estimated material cost
Estimated labor cost
Estimated total cost

Then allow the user to specify:

Desired profit margin

and calculate:

Suggested selling price

This should be a calculator only and should NOT automatically modify an order unless explicitly requested.

---

# 21. Inventory Alerts

Show warnings when inventory falls below the configured minimum.

Example:

LOW STOCK

Heavy cream
Current: 500 ml
Minimum: 1,000 ml

Mango pulp
Current: 300 g
Minimum: 500 g

---

# 22. Data Integrity

Financial calculations are important.

Use decimal/numeric database types for money.

DO NOT use floating-point values for currency calculations.

Use:

NUMERIC / Decimal

for:

* Prices
* Costs
* Revenue
* Profit

Store quantities using appropriate precision.

All financial calculations should be performed using Decimal-compatible logic.

---

# 23. Auditability

The application should make it possible to understand why a cost was calculated.

For an order, I should be able to click:

Ingredient Cost

and see:

Flour
250 g × $0.002/g = $0.50

Sugar
180 g × $0.0015/g = $0.27

Cream
300 ml × $0.006/ml = $1.80

etc.

Similarly, I should be able to see:

Labor:

4.2 hours × $20/hour = $84

This is important for debugging incorrect calculations.

---

# 24. Database Design

At minimum consider the following tables:

users
ingredients
ingredient_purchases
inventory_transactions
inventory_items
recipes
recipe_versions
recipe_ingredients
recipe_variants
cake_products
cake_components
orders
order_items
order_ingredient_usage
order_supply_usage
labor_entries
cost_categories
order_costs
payments

Do not blindly create every table.

Normalize the schema appropriately and document relationships.

Avoid premature complexity.

---

# 25. UI Structure

Main navigation:

Dashboard

Inventory

* Ingredients
* Supplies
* Purchases
* Inventory Transactions

Recipes

* Recipes
* Recipe Variants

Orders

* Orders
* New Order
* Order Profitability

Pricing

* Pricing Calculator

Analytics

* Daily
* Weekly
* Monthly

Settings

* Labor Rate
* Operating Costs
* Units
* Categories

---

# 26. UX Requirements

The application should be extremely simple for a non-technical business owner.

The user should NOT need to understand:

* SQL
* PostgreSQL
* APIs
* Database schemas
* Programming

Everything should be point-and-click.

For example:

Adding an ingredient:

Click:

Inventory → Add Ingredient

Enter:

Name:
Flour

Purchase quantity:
10

Purchase unit:
kg

Purchase price:
$14.99

Save.

The application automatically calculates the normalized cost.

---

# 27. Import / Export

Provide CSV export for:

* Ingredients
* Inventory
* Recipes
* Orders
* Profitability

Eventually support CSV import for ingredients and inventory.

The user must be able to back up their data.

---

# 28. Backup

Because this application contains business data, provide a simple database backup process.

The Docker setup should make it easy to create a PostgreSQL dump.

Document:

```bash
docker compose exec db pg_dump ...
```

or provide a convenient script such as:

```bash
./scripts/backup.sh
```

Also document how to restore the backup.

---

# 29. Local Development

The repository should have a clear structure similar to:

```text
cake-business-app/
│
├── frontend/
│
├── backend/
│
├── database/
│
├── migrations/
│
├── tests/
│
├── scripts/
│
├── docker-compose.yml
├── .env.example
├── README.md
└── PROJECT_SPEC.md
```

The exact structure can be improved if there is a better conventional approach.

---

# 30. Environment Configuration

Never hardcode:

* Database passwords
* Secret keys
* API keys
* Credentials

Use:

```text
.env
```

and provide:

```text
.env.example
```

The `.env` file must NOT be committed to Git.

---

# 31. Docker Requirements

Create Docker containers for:

Frontend
Backend
PostgreSQL

The database must use a persistent Docker volume.

The application should survive container restarts without losing data.

---

# 32. GitHub Repository Requirements

Create:

README.md

PROJECT_SPEC.md

ARCHITECTURE.md

DATABASE.md

API.md

DEVELOPMENT.md

TESTING.md

BACKUP.md

The README should explain how a completely new developer/user can:

1. Clone the repository
2. Install Docker Desktop
3. Configure `.env`
4. Start the application
5. Open the UI
6. Stop the application
7. Backup the database
8. Restore the database

---

# 33. AI Development Rules

GitHub Copilot will be used heavily to develop this application.

Copilot must follow these rules:

1. Do not rewrite large portions of the application unnecessarily.
2. Before making architectural changes, explain the proposed change.
3. Do not change the database schema without creating an Alembic migration.
4. Do not modify financial calculations without updating tests.
5. Do not introduce new dependencies without explaining why they are needed.
6. Prefer simple solutions over sophisticated frameworks.
7. Keep frontend and backend responsibilities separate.
8. Keep business logic in the backend.
9. Never hardcode business-specific prices.
10. Never hardcode ingredient costs.
11. Never use floating point for money.
12. Write tests for every important calculation.
13. Keep documentation updated when architecture changes.

---

# 34. Development Sequence

Do not implement everything simultaneously.

Implement in this order:

## Milestone 1

Project setup

* Git repository
* Docker
* PostgreSQL
* FastAPI
* React
* Basic UI
* Health check

## Milestone 2

Inventory

* Ingredients
* Supplies
* Purchases
* Inventory transactions
* Cost per unit

## Milestone 3

Recipes

* Recipes
* Recipe ingredients
* Recipe variants
* Recipe cost calculation

## Milestone 4

Orders

* Create order
* Select cake configuration
* Estimate cost

## Milestone 5

Actual usage

* Actual ingredient usage
* Actual supply usage
* Inventory deduction

## Milestone 6

Labor

* Default labor hours
* Actual labor hours
* Labor rate
* Labor cost

## Milestone 7

Profitability

* Revenue
* Material cost
* Labor cost
* Other costs
* Gross profit
* Profit margin

## Milestone 8

Dashboard

* Daily
* Weekly
* Monthly
* Profitability analytics

## Milestone 9

Pricing calculator

## Milestone 10

Backup/export/import

---

# 35. Definition of Done

A feature is NOT complete simply because the UI exists.

A feature is complete only when:

* Database model exists
* Migration exists
* Backend API exists
* Validation exists
* Business logic exists
* Frontend UI exists
* Error handling exists
* Tests exist
* Documentation is updated
* Docker environment works

---

# 36. First Task for Copilot

DO NOT start coding the entire application.

First analyze this specification and produce:

1. Finalized requirements
2. Assumptions
3. Questions/ambiguities
4. Recommended architecture
5. Database ERD
6. Database schema proposal
7. API endpoint proposal
8. Frontend page/component structure
9. Cost calculation methodology
10. Inventory calculation methodology
11. Profit calculation methodology
12. Docker architecture
13. Development milestones
14. Testing strategy
15. Risks and edge cases

Then wait for approval before implementing Milestone 1.

The application should be designed so that it can start as a local application but can later be deployed to a cloud environment without requiring a complete rewrite.

The primary goal is:

**A simple, reliable, personalized financial + inventory management system for a small cake business that tells me exactly how much each cake costs me, how much time I spent making it, how much I charged, and how much profit I actually made.**
