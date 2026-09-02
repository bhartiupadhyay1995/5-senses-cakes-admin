# Backend — FastAPI Application

Python-based REST API for 5 Senses Cakes business management application.

## Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- Alembic (migrations)
- Pydantic (validation)
- PostgreSQL

## Setup

### Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`  
API documentation at `http://localhost:8000/docs`

### Docker

```bash
docker build -t 5-senses-cakes-backend .
docker run -p 8000:8000 --env-file .env 5-senses-cakes-backend
```

## Testing

```bash
pytest

# With coverage
pytest --cov=app

# Specific test file
pytest tests/test_ingredients.py -v
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── database.py             # SQLAlchemy setup
│   ├── config.py               # Configuration
│   ├── api/
│   │   ├── __init__.py
│   │   ├── ingredients.py      # Ingredient endpoints
│   │   ├── recipes.py          # Recipe endpoints
│   │   ├── orders.py           # Order endpoints
│   │   ├── customers.py        # Customer endpoints
│   │   ├── analytics.py        # Analytics endpoints
│   │   └── router.py           # API router
│   ├── models/
│   │   ├── __init__.py
│   │   ├── ingredient.py       # Ingredient models
│   │   ├── recipe.py           # Recipe models
│   │   ├── order.py            # Order models
│   │   ├── customer.py         # Customer models
│   │   ├── base.py             # Base model
│   │   └── enums.py            # Enumerations
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── ingredient.py       # Ingredient Pydantic schemas
│   │   ├── recipe.py
│   │   ├── order.py
│   │   ├── customer.py
│   │   └── common.py           # Shared schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ingredient_service.py   # Business logic
│   │   ├── recipe_service.py
│   │   ├── order_service.py
│   │   ├── customer_service.py
│   │   ├── analytics_service.py
│   │   └── pricing_service.py
│   └── utils/
│       ├── __init__.py
│       ├── decorators.py       # Custom decorators
│       ├── exceptions.py       # Custom exceptions
│       └── calculations.py     # Calculation helpers
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Test fixtures
│   ├── test_ingredients.py
│   ├── test_recipes.py
│   ├── test_orders.py
│   ├── test_analytics.py
│   └── integration/
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

## Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Add new column"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic current
```

## API Documentation

See [API_SPECIFICATION.md](../docs/API_SPECIFICATION.md)

