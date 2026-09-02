// Core Entities
export interface User {
  id: number;
  name: string;
  email: string;
  hourly_rate: number;
  created_at: string;
  updated_at: string;
}

export interface Customer {
  id: number;
  name: string;
  email?: string;
  phone?: string;
  address?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

// Inventory
export interface Ingredient {
  id: number;
  name: string;
  category: string;
  base_unit: string;
  current_cost_per_unit: number;
  current_quantity: number;
  min_threshold: number;
  supplier?: string;
  active: boolean;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface InventoryTransaction {
  id: number;
  ingredient_id: number;
  transaction_type: 'PURCHASE' | 'CONSUMPTION' | 'ADJUSTMENT' | 'WASTE' | 'RETURN';
  quantity_change: number;
  transaction_date: string;
  purchase_price_per_unit?: number;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface CakeSupply {
  id: number;
  name: string;
  category: string;
  base_unit: string;
  current_cost_per_unit: number;
  current_quantity: number;
  min_threshold: number;
  supplier?: string;
  active: boolean;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface SupplyTransaction {
  id: number;
  supply_id: number;
  transaction_type: 'PURCHASE' | 'CONSUMPTION' | 'ADJUSTMENT' | 'WASTE' | 'RETURN';
  quantity_change: number;
  transaction_date: string;
  purchase_price_per_unit?: number;
  notes?: string;
  created_at: string;
  updated_at: string;
}

// Recipes
export interface Recipe {
  id: number;
  name: string;
  category: string;
  description?: string;
  active: boolean;
  created_at: string;
  updated_at: string;
}

export interface RecipeVariant {
  id: number;
  recipe_id: number;
  variant_name: string;
  base_yield: number;
  yield_unit: string;
  description?: string;
  active: boolean;
  created_at: string;
  updated_at: string;
}

export interface RecipeIngredient {
  id: number;
  recipe_variant_id: number;
  ingredient_id: number;
  quantity_required: number;
  unit: string;
  created_at: string;
  updated_at: string;
}

// Orders
export interface Order {
  id: number;
  customer_id: number;
  order_date: string;
  delivery_date: string;
  status: 'QUOTE' | 'CONFIRMED' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED';
  selling_price: number;
  discount_amount: number;
  tax_rate: number;
  tax_amount: number;
  deposit_amount: number;
  amount_paid: number;
  amount_remaining: number;
  estimated_total_cost: number;
  actual_total_cost?: number;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface OrderComponent {
  id: number;
  order_id: number;
  component_type: 'SPONGE' | 'FILLING' | 'FROSTING' | 'DECORATION' | 'PACKAGING';
  recipe_variant_id?: number;
  quantity: number;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface OrderIngredientUsage {
  id: number;
  order_id: number;
  ingredient_id: number;
  estimated_quantity: number;
  estimated_cost: number;
  actual_quantity?: number;
  actual_cost?: number;
  unit_used: string;
  created_at: string;
  updated_at: string;
}

export interface OrderSupplyUsage {
  id: number;
  order_id: number;
  supply_id: number;
  estimated_quantity: number;
  estimated_cost: number;
  actual_quantity?: number;
  actual_cost?: number;
  created_at: string;
  updated_at: string;
}

// Labor & Costs
export interface LaborEntry {
  id: number;
  order_id: number;
  activity: 'PREP' | 'BAKING' | 'FILLING' | 'FROSTING' | 'DECORATION' | 'CLEANUP';
  estimated_minutes: number;
  actual_minutes?: number;
  hourly_rate: number;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface OperatingCostCategory {
  id: number;
  name: string;
  description?: string;
  cost_type: 'FIXED_PER_ORDER' | 'USAGE_BASED';
  default_amount?: number;
  active: boolean;
  created_at: string;
  updated_at: string;
}

export interface OrderOperatingCost {
  id: number;
  order_id: number;
  operating_cost_category_id: number;
  estimated_amount: number;
  actual_amount?: number;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface OrderCostSummary {
  id: number;
  order_id: number;
  ingredient_cost_estimated: number;
  ingredient_cost_actual?: number;
  supply_cost_estimated: number;
  supply_cost_actual?: number;
  labor_cost_estimated: number;
  labor_cost_actual?: number;
  operating_cost_estimated: number;
  operating_cost_actual?: number;
  total_cost_estimated: number;
  total_cost_actual?: number;
  created_at: string;
  updated_at: string;
}

// Pagination
export interface PaginatedResponse<T> {
  data: T[];
  total?: number;
  skip?: number;
  limit?: number;
}

// API Response
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}
