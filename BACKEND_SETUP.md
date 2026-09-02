# 5 Senses Cakes Backend - Quick Start Guide

## Phase 3 Implementation: Backend API ✓ COMPLETE

This guide covers the setup and running of the Phase 3 backend implementation.

---

## What's Been Implemented

### ✅ API Infrastructure
- FastAPI application with full route organization
- Error handling middleware with proper exception mapping
- Request logging middleware
- CORS configuration
- Health check endpoint
- Structured API documentation

### ✅ Pydantic Schemas (Request/Response)
- Core domain: User, Customer
- Inventory domain: Ingredient, CakeSupply, InventoryTransaction, SupplyTransaction
- Recipe domain: Recipe, RecipeVariant, RecipeIngredient
- Order domain: Order, OrderComponent, OrderIngredientUsage, OrderSupplyUsage
- Labor & Costs: LaborEntry, OperatingCostCategory, OrderOperatingCost, OrderCostSummary

Each entity has:
- **Create** schema (for POST requests)
- **Update** schema (for PUT requests, all fields optional)
- **Response** schema (with timestamps and IDs)
- **List** schema (simplified for list responses)

### ✅ Repository Layer
- Base repository with generic CRUD operations
- Domain-specific repositories for advanced queries
- Repository factory for dependency injection
- Support for filtering, searching, and pagination

### ✅ REST API Endpoints

**Total Endpoints**: 80+

#### Core (User & Customer): 10 endpoints
- List, Get, Create, Update, Delete for Users and Customers
- Email uniqueness validation
- Customer search by name

#### Inventory: 22 endpoints
- Ingredient CRUD with active/inactive filtering
- Low stock ingredient detection
- Inventory transaction recording and history
- Cake supply CRUD
- Supply transaction tracking

#### Recipes: 15 endpoints
- Recipe CRUD with category filtering
- Recipe variant management with active/inactive filtering
- Recipe ingredient management
- Multiple units per ingredient support

#### Orders: 20 endpoints
- Order CRUD with status and customer filtering
- Upcoming deliveries view
- Order components management
- Ingredient usage tracking (estimated and actual)
- Supply usage tracking (estimated and actual)
- Automatic cost summary creation

#### Labor & Costs: 20+ endpoints
- Labor entry management with 6 activity types
- Estimated and actual time tracking
- Operating cost category management
- Order operating cost assignment
- Cost summary retrieval with denormalized totals

### ✅ Error Handling
- HTTPException for API-level errors (404, 409, 422)
- Middleware-based exception handling
- Database error mapping to appropriate HTTP status codes
- Validation error details with field-level information
- Consistent JSON error response format

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py                 # Settings and environment variables
│   ├── database.py               # Database connection management
│   ├── main.py                   # Application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py       # Dependency injection
│   │   ├── errors.py             # Custom error classes
│   │   └── routes/
│   │       ├── __init__.py       # Router registration
│   │       ├── core.py           # User, Customer endpoints
│   │       ├── inventory.py      # Ingredient, Supply endpoints
│   │       ├── recipe.py         # Recipe endpoints
│   │       ├── order.py          # Order endpoints
│   │       └── cost.py           # Labor, Cost endpoints
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── error_handling.py     # Exception handling & logging
│   ├── models/
│   │   ├── __init__.py           # Model exports
│   │   ├── base.py               # Base model
│   │   ├── user.py
│   │   ├── customer.py
│   │   ├── ingredient.py
│   │   ├── recipe.py
│   │   ├── order.py
│   │   ├── labor.py
│   │   ├── operating_cost.py
│   │   └── enums.py
│   ├── repositories/
│   │   ├── __init__.py           # Repository factory
│   │   ├── base.py               # Base repository
│   │   ├── core.py
│   │   ├── inventory.py
│   │   ├── recipe.py
│   │   ├── order.py
│   │   └── cost.py
│   └── schemas/
│       ├── __init__.py
│       ├── core.py
│       ├── inventory.py
│       ├── recipe.py
│       ├── order.py
│       ├── labor.py
│       └── cost.py
├── migrations/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 001_initial_schema.py
├── main.py                       # Application entry point
├── init_db.py                    # Database initialization
├── alembic.ini                   # Alembic configuration
├── run_migrations.sh             # Migration runner script
├── .env.example                  # Environment template
├── requirements.txt              # Python dependencies
├── Dockerfile
└── README.md
```

---

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

---

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your database configuration
# POSTGRES_USER=cakes_user
# POSTGRES_PASSWORD=your_password_here
# POSTGRES_DB=5_senses_cakes
# POSTGRES_HOST=localhost
# POSTGRES_PORT=5432
# BACKEND_HOST=0.0.0.0
# BACKEND_PORT=8000
# ENVIRONMENT=development
```

### 3. Initialize Database

#### Option A: Using Alembic (Recommended)
```bash
chmod +x run_migrations.sh
./run_migrations.sh
```

#### Option B: Direct Initialization
```bash
python init_db.py
```

### 4. Run the Application

```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

---

## API Access

Once the application is running:

- **Interactive Swagger UI**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **API Base URL**: http://localhost:8000/api/v1

---

## Testing the API

### Using curl

```bash
# Create a user
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "hourly_rate": 25.00
  }'

# List users
curl -X GET "http://localhost:8000/api/v1/users"

# Create a customer
curl -X POST "http://localhost:8000/api/v1/customers" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "email": "john@example.com",
    "phone": "555-1234"
  }'
```

### Using Python requests

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000/api/v1"

# Create user
response = requests.post(f"{BASE_URL}/users", json={
    "name": "Jane Doe",
    "email": "jane@example.com",
    "hourly_rate": 25.00
})
print(response.json())

# List users
response = requests.get(f"{BASE_URL}/users")
print(response.json())
```

---

## Common Tasks

### Create an Ingredient
```bash
curl -X POST "http://localhost:8000/api/v1/ingredients" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "All-Purpose Flour",
    "category": "Dry",
    "base_unit": "g",
    "current_cost_per_unit": 0.02,
    "current_quantity": 5000,
    "min_threshold": 1000,
    "supplier": "Local Mills",
    "active": true
  }'
```

### Create a Recipe
```bash
curl -X POST "http://localhost:8000/api/v1/recipes" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Vanilla Sponge",
    "category": "Sponge",
    "description": "Classic vanilla cake",
    "active": true
  }'
```

### Create an Order
```bash
curl -X POST "http://localhost:8000/api/v1/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "order_date": "2024-09-01",
    "delivery_date": "2024-09-15",
    "selling_price": 150.00,
    "estimated_total_cost": 85.00
  }'
```

---

## Troubleshooting

### Database Connection Error
```
Error: could not connect to server: Connection refused
```

**Solution**: Ensure PostgreSQL is running and connection details in `.env` are correct.

```bash
# On macOS
brew services start postgresql

# On Linux
sudo systemctl start postgresql

# Test connection
psql -U cakes_user -d 5_senses_cakes -h localhost
```

### Port Already in Use
```
Address already in use
```

**Solution**: Change the port in `.env` or kill the process using port 8000.

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Module Import Error
```
ModuleNotFoundError: No module named 'app'
```

**Solution**: Ensure you're in the `backend` directory and have installed dependencies.

```bash
cd backend
pip install -r requirements.txt
```

---

## Development Notes

### Adding a New Endpoint

1. **Define the schema** in `app/schemas/`
2. **Add repository methods** in `app/repositories/` if needed
3. **Create the route** in `app/api/routes/`
4. **Import and include** in `app/api/routes/__init__.py`

### Database Migrations

When the database schema changes:

```bash
# Create a migration
alembic revision --autogenerate -m "Description of changes"

# Review the generated migration in migrations/versions/

# Apply migrations
alembic upgrade head
```

### Testing

Currently, no test suite exists. Testing will be added in a future phase.

Recommended testing approach:
- Unit tests for repositories
- Integration tests for API endpoints
- Load testing for performance validation

---

## Next Steps

### Phase 4 - Frontend
- React + TypeScript UI
- Responsive design
- User-friendly forms for all entities
- Dashboard with key metrics
- Profitability analysis views

### Phase 5 - Analytics & Reporting
- Order profitability analysis
- Daily/Weekly/Monthly summaries
- Inventory value tracking
- Revenue vs. cost tracking
- Cost breakdown by order and component

### Phase 6 - Enhancement & Optimization
- Authentication and authorization
- User permissions
- Data export (CSV, PDF)
- Notifications for low stock
- Advanced search and filtering

---

## Support & Documentation

- **Full API Reference**: See `docs/API_REFERENCE.md`
- **Database Schema**: See `docs/DATABASE_SCHEMA.md`
- **Requirements & Architecture**: See `docs/PHASE_1_REQUIREMENTS_AND_ARCHITECTURE.md`
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Version

- **Phase 3 Version**: 0.1.0
- **Implementation Date**: September 2024
- **Status**: Complete ✓
