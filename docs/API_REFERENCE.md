# 5 Senses Cakes - REST API Documentation

## Overview

The 5 Senses Cakes API provides comprehensive endpoints for managing a personalized cake business including inventory, recipes, orders, labor tracking, and profitability analysis.

**API Base URL**: `/api/v1`

**API Documentation**: 
- Interactive Swagger UI: `/docs`
- ReDoc Documentation: `/redoc`
- Health Check: `/health`

---

## Authentication

Currently, the API is open (no authentication required). Authentication will be added in a future phase.

---

## Response Format

All responses follow a consistent JSON format:

### Success Response (200/201)
```json
{
  "id": 1,
  "field": "value",
  "created_at": "2024-09-01T00:00:00",
  "updated_at": "2024-09-01T00:00:00"
}
```

### Error Response (4xx/5xx)
```json
{
  "detail": "Error message describing what went wrong"
}
```

### Validation Error (422)
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "loc": ["body", "field_name"],
      "msg": "Error message",
      "type": "value_error"
    }
  ]
}
```

---

## Status Codes

- `200 OK` - Successful GET/PUT request
- `201 Created` - Successful POST request
- `204 No Content` - Successful DELETE request
- `400 Bad Request` - Invalid request format
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource already exists or constraint violation
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

---

## Pagination

List endpoints support pagination with query parameters:

```
GET /api/v1/customers?skip=0&limit=50
```

- `skip` (default: 0) - Number of records to skip
- `limit` (default: 100) - Maximum number of records to return

---

## Core Entities

### Users

Represents the business owner (single user application).

#### List Users
```
GET /api/v1/users
```

Query Parameters:
- `skip` (int, default: 0)
- `limit` (int, default: 100)

Response: Array of User objects

#### Get User
```
GET /api/v1/users/{user_id}
```

Response: User object

#### Create User
```
POST /api/v1/users
Content-Type: application/json

{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "hourly_rate": 25.00
}
```

Response: User object (201 Created)

#### Update User
```
PUT /api/v1/users/{user_id}
Content-Type: application/json

{
  "name": "Jane Smith",
  "hourly_rate": 30.00
}
```

Response: User object

#### Delete User
```
DELETE /api/v1/users/{user_id}
```

Response: 204 No Content

---

### Customers

Manages customer information for orders.

#### List Customers
```
GET /api/v1/customers?name=John
```

Query Parameters:
- `skip` (int, default: 0)
- `limit` (int, default: 100)
- `name` (string, optional) - Search by name (partial match)

Response: Array of Customer objects

#### Get Customer
```
GET /api/v1/customers/{customer_id}
```

Response: Customer object

#### Create Customer
```
POST /api/v1/customers
Content-Type: application/json

{
  "name": "John Smith",
  "email": "john@example.com",
  "phone": "555-1234",
  "address": "123 Main St",
  "notes": "Prefers chocolate cake"
}
```

Response: Customer object (201 Created)

#### Update Customer
```
PUT /api/v1/customers/{customer_id}
Content-Type: application/json

{
  "phone": "555-5678"
}
```

Response: Customer object

#### Delete Customer
```
DELETE /api/v1/customers/{customer_id}
```

Response: 204 No Content

---

## Inventory Management

### Ingredients

Manage food items used in recipes.

#### List Ingredients
```
GET /api/v1/ingredients?active_only=true
```

Query Parameters:
- `skip` (int, default: 0)
- `limit` (int, default: 100)
- `active_only` (boolean, default: false)

Response: Array of Ingredient objects

#### Get Low Stock Ingredients
```
GET /api/v1/ingredients/low-stock
```

Returns ingredients below minimum threshold.

Response: Array of Ingredient objects

#### Create Ingredient
```
POST /api/v1/ingredients
Content-Type: application/json

{
  "name": "All-Purpose Flour",
  "category": "Dry",
  "base_unit": "g",
  "current_cost_per_unit": 0.02,
  "current_quantity": 5000,
  "min_threshold": 1000,
  "supplier": "Local Mills",
  "active": true,
  "notes": "Store in cool, dry place"
}
```

Response: Ingredient object (201 Created)

#### Get Ingredient
```
GET /api/v1/ingredients/{ingredient_id}
```

Response: Ingredient object

#### Update Ingredient
```
PUT /api/v1/ingredients/{ingredient_id}
Content-Type: application/json

{
  "current_quantity": 4500,
  "current_cost_per_unit": 0.021
}
```

Response: Ingredient object

#### Delete Ingredient
```
DELETE /api/v1/ingredients/{ingredient_id}
```

Response: 204 No Content

---

### Inventory Transactions

Track ingredient purchases, usage, and adjustments.

#### Record Transaction
```
POST /api/v1/ingredients/{ingredient_id}/transactions
Content-Type: application/json

{
  "ingredient_id": 1,
  "transaction_type": "PURCHASE",
  "quantity_change": 1000,
  "transaction_date": "2024-09-01",
  "purchase_price_per_unit": 0.02,
  "notes": "Ordered from supplier"
}
```

Transaction types: PURCHASE, CONSUMPTION, ADJUSTMENT, WASTE, RETURN

Response: InventoryTransaction object (201 Created)

#### Get Ingredient Transactions
```
GET /api/v1/ingredients/{ingredient_id}/transactions
```

Query Parameters:
- `skip` (int, default: 0)
- `limit` (int, default: 100)

Response: Array of InventoryTransaction objects

---

### Cake Supplies

Manage non-food supplies (boxes, boards, toppers, etc.).

#### List Supplies
```
GET /api/v1/supplies?active_only=true
```

Query Parameters:
- `skip` (int, default: 0)
- `limit` (int, default: 100)
- `active_only` (boolean, default: false)

Response: Array of CakeSupply objects

#### Get Low Stock Supplies
```
GET /api/v1/supplies/low-stock
```

Response: Array of CakeSupply objects

#### Create Supply
```
POST /api/v1/supplies
Content-Type: application/json

{
  "name": "Cake Boxes - 10x10",
  "category": "Packaging",
  "unit": "box",
  "current_cost_per_unit": 0.50,
  "current_quantity": 200,
  "min_threshold": 50,
  "supplier": "Packaging Co",
  "active": true
}
```

Response: CakeSupply object (201 Created)

#### Update Supply
```
PUT /api/v1/supplies/{supply_id}
Content-Type: application/json

{
  "current_quantity": 150,
  "current_cost_per_unit": 0.55
}
```

Response: CakeSupply object

---

### Supply Transactions

Track supply purchases and usage.

#### Record Transaction
```
POST /api/v1/supplies/{supply_id}/transactions
Content-Type: application/json

{
  "supply_id": 1,
  "transaction_type": "PURCHASE",
  "quantity_change": 100,
  "transaction_date": "2024-09-01",
  "purchase_price_per_unit": 0.50
}
```

Response: SupplyTransaction object (201 Created)

---

## Recipes

### Create and manage cake recipes with variants.

#### List Recipes
```
GET /api/v1/recipes?category=Sponge&active_only=true
```

Query Parameters:
- `skip` (int, default: 0)
- `limit` (int, default: 100)
- `active_only` (boolean, default: false)
- `category` (string, optional)

Response: Array of Recipe objects

#### Create Recipe
```
POST /api/v1/recipes
Content-Type: application/json

{
  "name": "Vanilla Sponge",
  "category": "Sponge",
  "description": "Classic vanilla cake",
  "active": true
}
```

Response: Recipe object (201 Created)

#### Get Recipe
```
GET /api/v1/recipes/{recipe_id}
```

Response: Recipe object with variants and ingredients

---

### Recipe Variants

Different sizes or configurations of a recipe.

#### Create Variant
```
POST /api/v1/recipes/{recipe_id}/variants
Content-Type: application/json

{
  "recipe_id": 1,
  "variant_name": "6-inch 2-layer",
  "base_yield": 1,
  "yield_unit": "cake",
  "description": "Serves 8-10 people",
  "active": true
}
```

Response: RecipeVariant object (201 Created)

#### Get Recipe Variants
```
GET /api/v1/recipes/{recipe_id}/variants
```

Response: Array of RecipeVariant objects

#### Update Variant
```
PUT /api/v1/recipe-variants/{variant_id}
Content-Type: application/json

{
  "variant_name": "6-inch 3-layer"
}
```

Response: RecipeVariant object

---

### Recipe Ingredients

Ingredients required in a recipe variant.

#### Add Ingredient to Recipe
```
POST /api/v1/recipe-variants/{variant_id}/ingredients
Content-Type: application/json

{
  "ingredient_id": 1,
  "quantity_required": 200,
  "unit": "g"
}
```

Response: RecipeIngredient object (201 Created)

#### Get Recipe Ingredients
```
GET /api/v1/recipe-variants/{variant_id}/ingredients
```

Response: Array of RecipeIngredient objects

#### Remove Ingredient
```
DELETE /api/v1/recipe-ingredients/{ingredient_id}
```

Response: 204 No Content

---

## Orders

### Order Management

#### List Orders
```
GET /api/v1/orders?customer_id=1&status=CONFIRMED
```

Query Parameters:
- `skip` (int, default: 0)
- `limit` (int, default: 100)
- `customer_id` (int, optional)
- `status` (enum, optional) - QUOTE, CONFIRMED, IN_PROGRESS, COMPLETED, CANCELLED

Response: Array of Order objects

#### Get Upcoming Deliveries
```
GET /api/v1/orders/upcoming-deliveries
```

Response: Array of Order objects with CONFIRMED or IN_PROGRESS status

#### Create Order
```
POST /api/v1/orders
Content-Type: application/json

{
  "customer_id": 1,
  "order_date": "2024-09-01",
  "delivery_date": "2024-09-15",
  "status": "QUOTE",
  "selling_price": 150.00,
  "discount_amount": 0,
  "tax_rate": 10,
  "tax_amount": 15.00,
  "deposit_amount": 50.00,
  "amount_paid": 0,
  "amount_remaining": 165.00,
  "estimated_total_cost": 85.00,
  "notes": "Customer wants chocolate ganache"
}
```

Response: Order object (201 Created)

**Note**: OrderCostSummary is automatically created when an order is created.

#### Get Order
```
GET /api/v1/orders/{order_id}
```

Response: Order object with all components and usages

#### Update Order
```
PUT /api/v1/orders/{order_id}
Content-Type: application/json

{
  "status": "CONFIRMED",
  "amount_paid": 50.00,
  "amount_remaining": 115.00
}
```

Response: Order object

#### Delete Order
```
DELETE /api/v1/orders/{order_id}
```

Response: 204 No Content

---

### Order Components

Breakdown of what makes up an order (sponge, filling, frosting, etc.).

#### Add Component
```
POST /api/v1/orders/{order_id}/components
Content-Type: application/json

{
  "component_type": "SPONGE",
  "recipe_variant_id": 1,
  "quantity": 1,
  "notes": "Vanilla sponge"
}
```

Component types: SPONGE, FILLING, FROSTING, DECORATION, PACKAGING

Response: OrderComponent object (201 Created)

#### Get Order Components
```
GET /api/v1/orders/{order_id}/components
```

Response: Array of OrderComponent objects

---

### Order Ingredient Usage

Track ingredient usage for orders (estimated and actual).

#### Add Ingredient Usage
```
POST /api/v1/orders/{order_id}/ingredient-usages
Content-Type: application/json

{
  "ingredient_id": 1,
  "estimated_quantity": 250,
  "estimated_cost": 5.00,
  "unit_used": "g"
}
```

Response: OrderIngredientUsage object (201 Created)

#### Update Ingredient Usage (with actual values)
```
PUT /api/v1/order-ingredient-usages/{usage_id}
Content-Type: application/json

{
  "actual_quantity": 245,
  "actual_cost": 4.90
}
```

Response: OrderIngredientUsage object

---

### Order Supply Usage

Track supply usage for orders.

#### Add Supply Usage
```
POST /api/v1/orders/{order_id}/supply-usages
Content-Type: application/json

{
  "supply_id": 1,
  "estimated_quantity": 2,
  "estimated_cost": 1.00
}
```

Response: OrderSupplyUsage object (201 Created)

#### Update Supply Usage
```
PUT /api/v1/order-supply-usages/{usage_id}
Content-Type: application/json

{
  "actual_quantity": 2,
  "actual_cost": 1.00
}
```

Response: OrderSupplyUsage object

---

## Labor & Costs

### Labor Entries

Track labor activities for orders.

#### Add Labor Entry
```
POST /api/v1/orders/{order_id}/labor-entries
Content-Type: application/json

{
  "order_id": 1,
  "activity": "BAKING",
  "estimated_minutes": 60,
  "hourly_rate": 25.00,
  "notes": "Vanilla cake baking"
}
```

Activity types: PREP, BAKING, FILLING, FROSTING, DECORATION, CLEANUP

Response: LaborEntry object (201 Created)

#### Get Order Labor Entries
```
GET /api/v1/orders/{order_id}/labor-entries
```

Response: Array of LaborEntry objects with calculated estimated_cost

#### Update Labor Entry
```
PUT /api/v1/labor-entries/{labor_id}
Content-Type: application/json

{
  "actual_minutes": 55
}
```

Response: LaborEntry object with calculated actual_cost

---

### Operating Cost Categories

Define categories for operating expenses.

#### List Categories
```
GET /api/v1/operating-cost-categories?active_only=true
```

Query Parameters:
- `skip` (int, default: 0)
- `limit` (int, default: 100)
- `active_only` (boolean, default: false)

Response: Array of OperatingCostCategory objects

#### Create Category
```
POST /api/v1/operating-cost-categories
Content-Type: application/json

{
  "name": "Electricity",
  "description": "Electricity cost per order",
  "cost_type": "FIXED_PER_ORDER",
  "default_amount": 5.00,
  "active": true
}
```

Cost types: FIXED_PER_ORDER, USAGE_BASED

Response: OperatingCostCategory object (201 Created)

---

### Order Operating Costs

Assign operating costs to specific orders.

#### Add Operating Cost
```
POST /api/v1/orders/{order_id}/operating-costs
Content-Type: application/json

{
  "operating_cost_category_id": 1,
  "estimated_amount": 5.00
}
```

Response: OrderOperatingCost object (201 Created)

#### Get Order Operating Costs
```
GET /api/v1/orders/{order_id}/operating-costs
```

Response: Array of OrderOperatingCost objects

#### Update Operating Cost
```
PUT /api/v1/order-operating-costs/{cost_id}
Content-Type: application/json

{
  "actual_amount": 4.75
}
```

Response: OrderOperatingCost object

---

### Order Cost Summary

Denormalized view of total costs for an order.

#### Get Cost Summary
```
GET /api/v1/orders/{order_id}/cost-summary
```

Response:
```json
{
  "id": 1,
  "order_id": 1,
  "ingredient_cost_estimated": 25.00,
  "ingredient_cost_actual": 24.50,
  "supply_cost_estimated": 1.00,
  "supply_cost_actual": 1.00,
  "labor_cost_estimated": 25.00,
  "labor_cost_actual": 22.92,
  "operating_cost_estimated": 5.00,
  "operating_cost_actual": 4.75,
  "total_cost_estimated": 56.00,
  "total_cost_actual": 53.17,
  "created_at": "2024-09-01T00:00:00",
  "updated_at": "2024-09-01T00:00:00"
}
```

---

## Error Codes

### Common Errors

**404 Not Found**
```json
{
  "detail": "Entity with id {id} not found"
}
```

**409 Conflict (Already Exists)**
```json
{
  "detail": "Entity with {field} '{value}' already exists"
}
```

**422 Validation Error**
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "loc": ["body", "selling_price"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

**500 Internal Server Error**
```json
{
  "detail": "Internal server error"
}
```

---

## Examples

### Creating a Complete Order

1. Create an order:
```bash
POST /api/v1/orders
{
  "customer_id": 1,
  "order_date": "2024-09-01",
  "delivery_date": "2024-09-15",
  "selling_price": 150.00,
  "estimated_total_cost": 85.00
}
```

2. Add components:
```bash
POST /api/v1/orders/{order_id}/components
{
  "component_type": "SPONGE",
  "recipe_variant_id": 1,
  "quantity": 1
}
```

3. Add ingredient usage:
```bash
POST /api/v1/orders/{order_id}/ingredient-usages
{
  "ingredient_id": 1,
  "estimated_quantity": 250,
  "estimated_cost": 5.00,
  "unit_used": "g"
}
```

4. Add labor entries:
```bash
POST /api/v1/orders/{order_id}/labor-entries
{
  "activity": "BAKING",
  "estimated_minutes": 60,
  "hourly_rate": 25.00
}
```

5. Check cost summary:
```bash
GET /api/v1/orders/{order_id}/cost-summary
```

6. Update with actual values when order completes:
```bash
PUT /api/v1/order-ingredient-usages/{usage_id}
{
  "actual_quantity": 245,
  "actual_cost": 4.90
}

PUT /api/v1/labor-entries/{labor_id}
{
  "actual_minutes": 55
}

PUT /api/v1/orders/{order_id}
{
  "status": "COMPLETED"
}
```

---

## Rate Limiting & Performance

Currently, there are no rate limits applied to the API. Rate limiting will be added in a future phase based on actual usage patterns.

For better performance:
- Use pagination for list endpoints
- Filter results using query parameters when available
- Cache frequently accessed data on the client side

---

## Support

For issues or questions about the API, please refer to:
- Project documentation: `/docs` and `/redoc`
- Backend source code: `backend/app/api/routes/`
- Database models: `backend/app/models/`
