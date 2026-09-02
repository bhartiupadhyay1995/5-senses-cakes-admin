# API Specification
## 5 Senses Cakes Backend API

**Base URL**: `http://localhost:8000/api`  
**API Version**: v1  
**Content-Type**: `application/json`

---

## 1. Authentication & Authorization

### Current Phase (Phase 1)
- Single-user application
- No authentication required initially
- Architecture prepared for future authentication

### Future (Phase 3+)
- JWT-based authentication
- Role-based access control (RBAC)

---

## 2. Response Format

All API responses follow this structure:

### Success Response (2xx)
```json
{
  "data": { /* actual response data */ },
  "message": "Success message",
  "status": "success"
}
```

### Error Response (4xx, 5xx)
```json
{
  "error": "Error message",
  "details": { /* optional additional details */ },
  "status": "error",
  "code": "ERROR_CODE"
}
```

---

## 3. Inventory Endpoints

### 3.1 Ingredients

#### List Ingredients
```
GET /ingredients
Query Parameters:
  - category: string (optional)
  - active_only: boolean (default: true)
  - sort_by: string (default: "name")
  - skip: integer (default: 0)
  - limit: integer (default: 50)

Response: 200
{
  "data": [
    {
      "id": 1,
      "name": "All-purpose flour",
      "category": "Dry",
      "base_unit": "g",
      "current_cost_per_unit": 0.0015,
      "current_quantity": 5000,
      "min_threshold": 1000,
      "supplier": "Local Market",
      "active": true,
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z"
    }
  ],
  "total": 42,
  "message": "Ingredients retrieved successfully"
}
```

#### Get Ingredient Details
```
GET /ingredients/{ingredient_id}

Response: 200
{
  "data": {
    "id": 1,
    "name": "All-purpose flour",
    "category": "Dry",
    "base_unit": "g",
    "current_cost_per_unit": 0.0015,
    "current_quantity": 5000,
    "min_threshold": 1000,
    "supplier": "Local Market",
    "active": true,
    "available_units": [
      { "unit": "g", "conversion_to_base": 1 },
      { "unit": "kg", "conversion_to_base": 1000 },
      { "unit": "cup", "conversion_to_base": 125 }
    ],
    "transaction_history": [
      {
        "id": 101,
        "transaction_type": "PURCHASE",
        "quantity_change": 5000,
        "transaction_date": "2024-01-15",
        "purchase_price_per_unit": 0.0015,
        "notes": "Bought from supplier A"
      }
    ],
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
  }
}
```

#### Create Ingredient
```
POST /ingredients

Request Body:
{
  "name": "Vanilla Extract",
  "category": "Liquid",
  "base_unit": "ml",
  "current_cost_per_unit": 0.05,
  "current_quantity": 100,
  "min_threshold": 50,
  "supplier": "Local Market",
  "available_units": [
    { "unit": "ml", "conversion_to_base": 1 },
    { "unit": "tsp", "conversion_to_base": 5 },
    { "unit": "tbsp", "conversion_to_base": 15 }
  ]
}

Response: 201
{
  "data": {
    "id": 2,
    "name": "Vanilla Extract",
    "category": "Liquid",
    "base_unit": "ml",
    "current_cost_per_unit": 0.05,
    "current_quantity": 100,
    "min_threshold": 50,
    "supplier": "Local Market",
    "active": true,
    "created_at": "2024-01-16T10:00:00Z"
  },
  "message": "Ingredient created successfully"
}
```

#### Update Ingredient
```
PUT /ingredients/{ingredient_id}

Request Body:
{
  "current_cost_per_unit": 0.048,  # updated price
  "min_threshold": 60,
  "supplier": "New Supplier"
}

Response: 200
{
  "data": { /* updated ingredient */ },
  "message": "Ingredient updated successfully"
}
```

#### Delete Ingredient (Soft Delete)
```
DELETE /ingredients/{ingredient_id}

Response: 200
{
  "data": { "id": 1, "active": false },
  "message": "Ingredient deactivated successfully"
}
```

### 3.2 Inventory Transactions

#### Record Transaction
```
POST /inventory-transactions

Request Body:
{
  "ingredient_id": 1,
  "transaction_type": "CONSUMPTION",  # or PURCHASE, ADJUSTMENT, WASTE, RETURN
  "quantity_change": -250,
  "transaction_date": "2024-01-16",
  "purchase_price_per_unit": null,  # only for PURCHASE
  "notes": "Used for vanilla sponge"
}

Response: 201
{
  "data": {
    "id": 102,
    "ingredient_id": 1,
    "transaction_type": "CONSUMPTION",
    "quantity_change": -250,
    "transaction_date": "2024-01-16",
    "notes": "Used for vanilla sponge",
    "created_at": "2024-01-16T14:30:00Z"
  },
  "updated_inventory": 4750,
  "message": "Transaction recorded successfully"
}
```

#### Get Ingredient Transaction History
```
GET /ingredients/{ingredient_id}/transactions
Query Parameters:
  - start_date: string (YYYY-MM-DD)
  - end_date: string (YYYY-MM-DD)
  - transaction_type: string (optional: PURCHASE|CONSUMPTION|ADJUSTMENT|WASTE|RETURN)
  - skip: integer (default: 0)
  - limit: integer (default: 100)

Response: 200
{
  "data": [
    {
      "id": 102,
      "transaction_type": "CONSUMPTION",
      "quantity_change": -250,
      "transaction_date": "2024-01-16",
      "purchase_price_per_unit": null,
      "notes": "Used for vanilla sponge",
      "created_at": "2024-01-16T14:30:00Z"
    }
  ],
  "total": 15,
  "current_inventory": 4750,
  "message": "Transactions retrieved successfully"
}
```

### 3.3 Cake Supplies

Similar endpoints to Ingredients (`/supplies`)

---

## 4. Recipe Endpoints

### 4.1 Recipes

#### List Recipes
```
GET /recipes
Query Parameters:
  - category: string (optional)
  - active_only: boolean (default: true)

Response: 200
{
  "data": [
    {
      "id": 1,
      "name": "Vanilla Sponge",
      "category": "Sponge",
      "description": "Classic vanilla sponge cake",
      "active": true,
      "variants": [
        {
          "id": 10,
          "variant_name": "6-inch 2-layer",
          "base_yield": 1,
          "yield_unit": "cake"
        }
      ],
      "created_at": "2024-01-01T10:00:00Z"
    }
  ]
}
```

#### Get Recipe with Variants and Ingredients
```
GET /recipes/{recipe_id}

Response: 200
{
  "data": {
    "id": 1,
    "name": "Vanilla Sponge",
    "category": "Sponge",
    "description": "Classic vanilla sponge cake",
    "active": true,
    "variants": [
      {
        "id": 10,
        "variant_name": "6-inch 2-layer",
        "base_yield": 1,
        "yield_unit": "cake",
        "ingredients": [
          {
            "id": 100,
            "ingredient_id": 1,
            "ingredient_name": "All-purpose flour",
            "quantity_required": 250,
            "unit": "g",
            "current_cost_per_unit": 0.0015,
            "estimated_cost": 0.375
          },
          {
            "id": 101,
            "ingredient_id": 5,
            "ingredient_name": "Granulated sugar",
            "quantity_required": 180,
            "unit": "g",
            "current_cost_per_unit": 0.002,
            "estimated_cost": 0.36
          }
        ],
        "total_estimated_cost": 2.85
      }
    ]
  }
}
```

#### Create Recipe
```
POST /recipes

Request Body:
{
  "name": "Chocolate Ganache",
  "category": "Frosting",
  "description": "Rich chocolate ganache frosting"
}

Response: 201
{
  "data": { /* created recipe */ }
}
```

### 4.2 Recipe Variants

#### Add Recipe Variant
```
POST /recipes/{recipe_id}/variants

Request Body:
{
  "variant_name": "8-inch 3-layer",
  "base_yield": 1,
  "yield_unit": "cake",
  "description": "Larger variant for 8-inch cake"
}

Response: 201
{
  "data": { /* created variant */ }
}
```

#### Add Ingredient to Variant
```
POST /recipes/{recipe_id}/variants/{variant_id}/ingredients

Request Body:
{
  "ingredient_id": 3,
  "quantity_required": 300,
  "unit": "g"
}

Response: 201
{
  "data": { /* ingredient added to variant */ }
}
```

#### Calculate Recipe Cost
```
GET /recipes/{recipe_id}/variants/{variant_id}/cost

Response: 200
{
  "data": {
    "variant_name": "6-inch 2-layer",
    "ingredients": [
      {
        "ingredient_name": "Flour",
        "quantity": 250,
        "unit": "g",
        "unit_cost": 0.0015,
        "line_cost": 0.375
      }
    ],
    "total_cost": 2.85
  }
}
```

---

## 5. Order Endpoints

### 5.1 Orders

#### List Orders
```
GET /orders
Query Parameters:
  - customer_id: integer (optional)
  - status: string (optional: QUOTE|CONFIRMED|IN_PROGRESS|COMPLETED|CANCELLED)
  - start_date: string (YYYY-MM-DD, optional)
  - end_date: string (YYYY-MM-DD, optional)
  - skip: integer (default: 0)
  - limit: integer (default: 50)

Response: 200
{
  "data": [
    {
      "id": 1001,
      "customer_id": 50,
      "customer_name": "Jane Doe",
      "order_date": "2024-01-16",
      "delivery_date": "2024-01-18",
      "status": "CONFIRMED",
      "selling_price": 85.00,
      "discount_amount": 0,
      "tax_amount": 0,
      "deposit_amount": 42.50,
      "amount_paid": 42.50,
      "amount_remaining": 42.50,
      "estimated_total_cost": 28.50,
      "actual_total_cost": null,
      "created_at": "2024-01-16T10:00:00Z"
    }
  ],
  "total": 8
}
```

#### Get Order Details
```
GET /orders/{order_id}

Response: 200
{
  "data": {
    "id": 1001,
    "customer_id": 50,
    "customer_name": "Jane Doe",
    "customer_contact": {
      "email": "jane@example.com",
      "phone": "555-1234"
    },
    "order_date": "2024-01-16",
    "delivery_date": "2024-01-18",
    "status": "CONFIRMED",
    "selling_price": 85.00,
    "discount_amount": 0,
    "tax_amount": 0,
    "deposit_amount": 42.50,
    "amount_paid": 42.50,
    "amount_remaining": 42.50,
    "components": [
      {
        "id": 5001,
        "component_type": "SPONGE",
        "recipe_variant_id": 10,
        "recipe_variant_name": "6-inch 2-layer",
        "quantity": 1
      },
      {
        "id": 5002,
        "component_type": "FILLING",
        "recipe_variant_id": 12,
        "recipe_variant_name": "Strawberry Filling",
        "quantity": 1
      }
    ],
    "estimated_costs": {
      "ingredient_cost": 12.50,
      "supply_cost": 5.00,
      "labor_cost": 10.00,
      "operating_cost": 1.00,
      "total": 28.50
    },
    "actual_costs": null,
    "labor_entries": [
      {
        "activity": "PREP",
        "estimated_minutes": 30,
        "actual_minutes": null,
        "hourly_rate": 20.00
      }
    ],
    "notes": "Customer prefers pink decoration"
  }
}
```

#### Create Order
```
POST /orders

Request Body:
{
  "customer_id": 50,
  "order_date": "2024-01-16",
  "delivery_date": "2024-01-18",
  "selling_price": 85.00,
  "discount_amount": 0,
  "deposit_amount": 42.50,
  "notes": "Customer prefers pink decoration",
  "components": [
    {
      "component_type": "SPONGE",
      "recipe_variant_id": 10
    },
    {
      "component_type": "FILLING",
      "recipe_variant_id": 12
    }
  ]
}

Response: 201
{
  "data": { /* created order */ },
  "estimated_cost": 28.50,
  "message": "Order created successfully"
}
```

#### Update Order
```
PUT /orders/{order_id}

Request Body:
{
  "selling_price": 90.00,
  "discount_amount": 5.00,
  "status": "IN_PROGRESS"
}

Response: 200
{
  "data": { /* updated order */ }
}
```

#### Update Order Status
```
PUT /orders/{order_id}/status

Request Body:
{
  "status": "IN_PROGRESS"  # or COMPLETED, CANCELLED
}

Response: 200
{
  "data": { /* updated order */ }
}
```

### 5.2 Order Components

#### Add Component to Order
```
POST /orders/{order_id}/components

Request Body:
{
  "component_type": "DECORATION",
  "supply_id": 30,
  "quantity": 2
}

Response: 201
{
  "data": { /* created component */ }
}
```

### 5.3 Order Labor

#### Record Labor Entry
```
POST /orders/{order_id}/labor

Request Body:
{
  "activity": "PREP",
  "estimated_minutes": 30,
  "actual_minutes": 35  # optional, recorded when work done
}

Response: 201
{
  "data": {
    "id": 2001,
    "order_id": 1001,
    "activity": "PREP",
    "estimated_minutes": 30,
    "actual_minutes": 35,
    "hourly_rate": 20.00,
    "estimated_cost": 10.00,
    "actual_cost": 11.67
  }
}
```

### 5.4 Order Ingredient Usage

#### Record Ingredient Usage
```
POST /orders/{order_id}/ingredient-usage

Request Body:
{
  "ingredient_id": 1,
  "actual_quantity": 260  # exceeded estimate of 250
}

Response: 201
{
  "data": {
    "ingredient_id": 1,
    "ingredient_name": "All-purpose flour",
    "estimated_quantity": 250,
    "estimated_cost": 0.375,
    "actual_quantity": 260,
    "actual_cost": 0.39,
    "difference": 0.015
  }
}
```

### 5.5 Order Profitability

#### Get Order Cost Breakdown
```
GET /orders/{order_id}/costs

Response: 200
{
  "data": {
    "order_id": 1001,
    "revenue": 85.00,
    "costs": {
      "ingredients": {
        "estimated": 12.50,
        "actual": 13.20,
        "breakdown": [
          {
            "ingredient": "Flour",
            "quantity": 260,
            "unit_cost": 0.0015,
            "total": 0.39
          }
        ]
      },
      "supplies": {
        "estimated": 5.00,
        "actual": 5.00
      },
      "labor": {
        "estimated": 10.00,
        "actual": 11.67,
        "breakdown": [
          {
            "activity": "PREP",
            "hours": 0.583,
            "rate": 20.00,
            "cost": 11.67
          }
        ]
      },
      "operating": {
        "estimated": 1.00,
        "actual": 1.00
      }
    },
    "total_cost": 31.87,
    "gross_profit": 53.13,
    "profit_margin": 62.51
  }
}
```

#### Get Order Profitability Summary
```
GET /orders/{order_id}/profitability

Response: 200
{
  "data": {
    "order_id": 1001,
    "customer_name": "Jane Doe",
    "status": "COMPLETED",
    "revenue": 85.00,
    "ingredients_cost": 13.20,
    "supplies_cost": 5.00,
    "labor_cost": 11.67,
    "operating_cost": 1.00,
    "total_cost": 30.87,
    "gross_profit": 54.13,
    "profit_margin": 63.68,
    "status_label": "Highly Profitable"
  }
}
```

---

## 6. Customer Endpoints

#### List Customers
```
GET /customers
Query Parameters:
  - skip: integer (default: 0)
  - limit: integer (default: 50)

Response: 200
{
  "data": [
    {
      "id": 50,
      "name": "Jane Doe",
      "email": "jane@example.com",
      "phone": "555-1234",
      "address": "123 Main St",
      "order_count": 3,
      "total_spent": 250.00,
      "created_at": "2024-01-01T10:00:00Z"
    }
  ],
  "total": 12
}
```

#### Get Customer Details
```
GET /customers/{customer_id}

Response: 200
{
  "data": {
    "id": 50,
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "555-1234",
    "address": "123 Main St",
    "notes": "Prefers chocolate flavors",
    "order_count": 3,
    "total_spent": 250.00,
    "orders": [
      {
        "id": 1001,
        "order_date": "2024-01-16",
        "status": "COMPLETED",
        "selling_price": 85.00
      }
    ],
    "created_at": "2024-01-01T10:00:00Z"
  }
}
```

#### Create Customer
```
POST /customers

Request Body:
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "555-1234",
  "address": "123 Main St",
  "notes": "Prefers chocolate flavors"
}

Response: 201
{
  "data": { /* created customer */ }
}
```

---

## 7. Analytics Endpoints

### 7.1 Dashboard Metrics

#### Get Dashboard Data
```
GET /analytics/dashboard?period=today

Query Parameters:
  - period: string (required: today|week|month)

Response: 200
{
  "data": {
    "period": "today",
    "date_range": {
      "start": "2024-01-16",
      "end": "2024-01-16"
    },
    "summary": {
      "orders_count": 2,
      "orders_completed": 1,
      "revenue": 85.00,
      "total_cost": 30.87,
      "gross_profit": 54.13,
      "hours_worked": 4.5
    },
    "top_metrics": {
      "average_profit_per_order": 54.13,
      "average_order_value": 42.50,
      "profit_margin": 63.68
    }
  }
}
```

### 7.2 Profitability Analysis

#### Get Profitability by Period
```
GET /analytics/profitability?start_date=2024-01-01&end_date=2024-01-31

Query Parameters:
  - start_date: string (YYYY-MM-DD)
  - end_date: string (YYYY-MM-DD)

Response: 200
{
  "data": {
    "period": "2024-01-01 to 2024-01-31",
    "summary": {
      "total_revenue": 850.00,
      "total_cost": 275.00,
      "gross_profit": 575.00,
      "profit_margin": 67.65,
      "order_count": 10,
      "average_profit_per_order": 57.50
    },
    "daily_breakdown": [
      {
        "date": "2024-01-16",
        "revenue": 85.00,
        "cost": 30.87,
        "profit": 54.13,
        "order_count": 1
      }
    ]
  }
}
```

### 7.3 Order Analytics

#### Get Order Analysis
```
GET /analytics/orders?start_date=2024-01-01&end_date=2024-01-31&sort_by=profit

Query Parameters:
  - start_date: string (YYYY-MM-DD)
  - end_date: string (YYYY-MM-DD)
  - sort_by: string (profit|revenue|time|date)
  - filter_status: string (optional)

Response: 200
{
  "data": {
    "most_profitable": [
      {
        "order_id": 1005,
        "customer_name": "Jane Doe",
        "revenue": 120.00,
        "cost": 35.00,
        "profit": 85.00,
        "margin": 70.83
      }
    ],
    "least_profitable": [
      {
        "order_id": 1001,
        "customer_name": "John Smith",
        "revenue": 75.00,
        "cost": 50.00,
        "profit": 25.00,
        "margin": 33.33
      }
    ],
    "highest_revenue": [
      {
        "order_id": 1010,
        "customer_name": "Corporate Event",
        "revenue": 250.00,
        "cost": 120.00,
        "profit": 130.00
      }
    ]
  }
}
```

### 7.4 Inventory Analytics

#### Get Inventory Usage
```
GET /analytics/inventory-usage?start_date=2024-01-01&end_date=2024-01-31

Response: 200
{
  "data": {
    "most_used_ingredients": [
      {
        "ingredient_id": 1,
        "name": "All-purpose flour",
        "quantity_used": 5000,
        "unit": "g",
        "cost": 7.50,
        "orders_count": 8
      }
    ],
    "low_stock_items": [
      {
        "ingredient_id": 5,
        "name": "Vanilla Extract",
        "current_quantity": 45,
        "min_threshold": 50,
        "status": "BELOW_MINIMUM"
      }
    ]
  }
}
```

### 7.5 Customer Analytics

#### Get Customer Analysis
```
GET /analytics/customers?start_date=2024-01-01&end_date=2024-01-31

Response: 200
{
  "data": {
    "recurring_customers": [
      {
        "customer_id": 50,
        "name": "Jane Doe",
        "order_count": 3,
        "total_spent": 250.00,
        "average_order_value": 83.33,
        "last_order": "2024-01-16",
        "profit_from_customer": 175.00
      }
    ],
    "new_customers": [
      {
        "customer_id": 51,
        "name": "John Smith",
        "first_order": "2024-01-15",
        "order_value": 75.00
      }
    ]
  }
}
```

---

## 8. Pricing Calculator

#### Calculate Suggested Price
```
POST /pricing-calculator/estimate

Request Body:
{
  "components": [
    {
      "component_type": "SPONGE",
      "recipe_variant_id": 10
    },
    {
      "component_type": "FILLING",
      "recipe_variant_id": 12
    }
  ],
  "labor_time_minutes": 270,
  "desired_profit_margin": 65  # percentage
}

Response: 200
{
  "data": {
    "estimated_ingredient_cost": 12.50,
    "estimated_supply_cost": 5.00,
    "estimated_labor_cost": 10.00,
    "estimated_operating_cost": 1.00,
    "total_estimated_cost": 28.50,
    "desired_profit_margin": 65,
    "suggested_selling_price": 81.43,
    "calculation_breakdown": {
      "total_cost": 28.50,
      "cost_plus_margin": "28.50 × (1 + 0.65) = 47.03",
      "markup_multiplier": 1.65,
      "suggested_price": 81.43
    }
  }
}
```

---

## 9. Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| INGREDIENT_NOT_FOUND | 404 | Ingredient does not exist |
| INVALID_QUANTITY | 400 | Invalid quantity value |
| INSUFFICIENT_INVENTORY | 400 | Not enough inventory for consumption |
| ORDER_NOT_FOUND | 404 | Order does not exist |
| INVALID_ORDER_STATUS | 400 | Invalid status transition |
| RECIPE_NOT_FOUND | 404 | Recipe does not exist |
| CUSTOMER_NOT_FOUND | 404 | Customer does not exist |
| DATABASE_ERROR | 500 | Database operation failed |
| VALIDATION_ERROR | 400 | Request validation failed |

