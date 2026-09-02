import axios, { AxiosInstance, AxiosError } from 'axios';

const API_BASE_URL = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000/api/v1';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add error handling interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        // Handle common errors
        if (error.response?.status === 401) {
          // Redirect to login if needed
          console.error('Unauthorized - redirecting to login');
        }
        return Promise.reject(error);
      }
    );
  }

  // Users
  getUsers(skip = 0, limit = 100) {
    return this.client.get('/users', { params: { skip, limit } });
  }

  getUser(id: number) {
    return this.client.get(`/users/${id}`);
  }

  createUser(data: any) {
    return this.client.post('/users', data);
  }

  updateUser(id: number, data: any) {
    return this.client.put(`/users/${id}`, data);
  }

  deleteUser(id: number) {
    return this.client.delete(`/users/${id}`);
  }

  // Customers
  getCustomers(skip = 0, limit = 100, name?: string) {
    return this.client.get('/customers', { params: { skip, limit, name } });
  }

  getCustomer(id: number) {
    return this.client.get(`/customers/${id}`);
  }

  createCustomer(data: any) {
    return this.client.post('/customers', data);
  }

  updateCustomer(id: number, data: any) {
    return this.client.put(`/customers/${id}`, data);
  }

  deleteCustomer(id: number) {
    return this.client.delete(`/customers/${id}`);
  }

  // Ingredients
  getIngredients(skip = 0, limit = 100, activeOnly = false) {
    return this.client.get('/ingredients', { params: { skip, limit, active_only: activeOnly } });
  }

  getLowStockIngredients() {
    return this.client.get('/ingredients/low-stock');
  }

  getIngredient(id: number) {
    return this.client.get(`/ingredients/${id}`);
  }

  createIngredient(data: any) {
    return this.client.post('/ingredients', data);
  }

  updateIngredient(id: number, data: any) {
    return this.client.put(`/ingredients/${id}`, data);
  }

  deleteIngredient(id: number) {
    return this.client.delete(`/ingredients/${id}`);
  }

  getIngredientTransactions(ingredientId: number, skip = 0, limit = 100) {
    return this.client.get(`/ingredients/${ingredientId}/transactions`, {
      params: { skip, limit },
    });
  }

  createIngredientTransaction(ingredientId: number, data: any) {
    return this.client.post(`/ingredients/${ingredientId}/transactions`, data);
  }

  // Cake Supplies
  getSupplies(skip = 0, limit = 100, activeOnly = false) {
    return this.client.get('/supplies', { params: { skip, limit, active_only: activeOnly } });
  }

  getLowStockSupplies() {
    return this.client.get('/supplies/low-stock');
  }

  getSupply(id: number) {
    return this.client.get(`/supplies/${id}`);
  }

  createSupply(data: any) {
    return this.client.post('/supplies', data);
  }

  updateSupply(id: number, data: any) {
    return this.client.put(`/supplies/${id}`, data);
  }

  deleteSupply(id: number) {
    return this.client.delete(`/supplies/${id}`);
  }

  getSupplyTransactions(supplyId: number, skip = 0, limit = 100) {
    return this.client.get(`/supplies/${supplyId}/transactions`, { params: { skip, limit } });
  }

  createSupplyTransaction(supplyId: number, data: any) {
    return this.client.post(`/supplies/${supplyId}/transactions`, data);
  }

  // Recipes
  getRecipes(skip = 0, limit = 100, category?: string, activeOnly = false) {
    return this.client.get('/recipes', {
      params: { skip, limit, category, active_only: activeOnly },
    });
  }

  getRecipe(id: number) {
    return this.client.get(`/recipes/${id}`);
  }

  createRecipe(data: any) {
    return this.client.post('/recipes', data);
  }

  updateRecipe(id: number, data: any) {
    return this.client.put(`/recipes/${id}`, data);
  }

  deleteRecipe(id: number) {
    return this.client.delete(`/recipes/${id}`);
  }

  // Recipe Variants
  getRecipeVariants(recipeId: number) {
    return this.client.get(`/recipes/${recipeId}/variants`);
  }

  getRecipeVariant(variantId: number) {
    return this.client.get(`/recipe-variants/${variantId}`);
  }

  createRecipeVariant(recipeId: number, data: any) {
    return this.client.post(`/recipes/${recipeId}/variants`, data);
  }

  updateRecipeVariant(variantId: number, data: any) {
    return this.client.put(`/recipe-variants/${variantId}`, data);
  }

  deleteRecipeVariant(variantId: number) {
    return this.client.delete(`/recipe-variants/${variantId}`);
  }

  // Recipe Ingredients
  getRecipeIngredients(variantId: number) {
    return this.client.get(`/recipe-variants/${variantId}/ingredients`);
  }

  addRecipeIngredient(variantId: number, data: any) {
    return this.client.post(`/recipe-variants/${variantId}/ingredients`, data);
  }

  removeRecipeIngredient(ingredientId: number) {
    return this.client.delete(`/recipe-ingredients/${ingredientId}`);
  }

  // Orders
  getOrders(skip = 0, limit = 100, customerId?: number, status?: string) {
    return this.client.get('/orders', { params: { skip, limit, customer_id: customerId, status } });
  }

  getUpcomingDeliveries() {
    return this.client.get('/orders/upcoming-deliveries');
  }

  getOrder(id: number) {
    return this.client.get(`/orders/${id}`);
  }

  createOrder(data: any) {
    return this.client.post('/orders', data);
  }

  updateOrder(id: number, data: any) {
    return this.client.put(`/orders/${id}`, data);
  }

  deleteOrder(id: number) {
    return this.client.delete(`/orders/${id}`);
  }

  // Order Components
  getOrderComponents(orderId: number) {
    return this.client.get(`/orders/${orderId}/components`);
  }

  addOrderComponent(orderId: number, data: any) {
    return this.client.post(`/orders/${orderId}/components`, data);
  }

  updateOrderComponent(componentId: number, data: any) {
    return this.client.put(`/order-components/${componentId}`, data);
  }

  deleteOrderComponent(componentId: number) {
    return this.client.delete(`/order-components/${componentId}`);
  }

  // Order Ingredient Usage
  getOrderIngredientUsages(orderId: number) {
    return this.client.get(`/orders/${orderId}/ingredient-usages`);
  }

  addOrderIngredientUsage(orderId: number, data: any) {
    return this.client.post(`/orders/${orderId}/ingredient-usages`, data);
  }

  updateOrderIngredientUsage(usageId: number, data: any) {
    return this.client.put(`/order-ingredient-usages/${usageId}`, data);
  }

  // Order Supply Usage
  getOrderSupplyUsages(orderId: number) {
    return this.client.get(`/orders/${orderId}/supply-usages`);
  }

  addOrderSupplyUsage(orderId: number, data: any) {
    return this.client.post(`/orders/${orderId}/supply-usages`, data);
  }

  updateOrderSupplyUsage(usageId: number, data: any) {
    return this.client.put(`/order-supply-usages/${usageId}`, data);
  }

  // Labor Entries
  getOrderLaborEntries(orderId: number) {
    return this.client.get(`/orders/${orderId}/labor-entries`);
  }

  addLaborEntry(orderId: number, data: any) {
    return this.client.post(`/orders/${orderId}/labor-entries`, data);
  }

  updateLaborEntry(laborId: number, data: any) {
    return this.client.put(`/labor-entries/${laborId}`, data);
  }

  deleteLaborEntry(laborId: number) {
    return this.client.delete(`/labor-entries/${laborId}`);
  }

  // Operating Cost Categories
  getOperatingCostCategories(skip = 0, limit = 100, activeOnly = false) {
    return this.client.get('/operating-cost-categories', {
      params: { skip, limit, active_only: activeOnly },
    });
  }

  getOperatingCostCategory(id: number) {
    return this.client.get(`/operating-cost-categories/${id}`);
  }

  createOperatingCostCategory(data: any) {
    return this.client.post('/operating-cost-categories', data);
  }

  updateOperatingCostCategory(id: number, data: any) {
    return this.client.put(`/operating-cost-categories/${id}`, data);
  }

  deleteOperatingCostCategory(id: number) {
    return this.client.delete(`/operating-cost-categories/${id}`);
  }

  // Order Operating Costs
  getOrderOperatingCosts(orderId: number) {
    return this.client.get(`/orders/${orderId}/operating-costs`);
  }

  addOrderOperatingCost(orderId: number, data: any) {
    return this.client.post(`/orders/${orderId}/operating-costs`, data);
  }

  updateOrderOperatingCost(costId: number, data: any) {
    return this.client.put(`/order-operating-costs/${costId}`, data);
  }

  deleteOrderOperatingCost(costId: number) {
    return this.client.delete(`/order-operating-costs/${costId}`);
  }

  // Order Cost Summary
  getOrderCostSummary(orderId: number) {
    return this.client.get(`/orders/${orderId}/cost-summary`);
  }
}

export const apiClient = new ApiClient();
