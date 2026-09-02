import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../api/client';

// Users
export const useUsers = (skip = 0, limit = 100) => {
  return useQuery({
    queryKey: ['users', skip, limit],
    queryFn: () => apiClient.getUsers(skip, limit),
    select: (response) => response.data,
  });
};

export const useUser = (id: number) => {
  return useQuery({
    queryKey: ['users', id],
    queryFn: () => apiClient.getUser(id),
    select: (response) => response.data,
  });
};

export const useCreateUser = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: any) => apiClient.createUser(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
};

export const useUpdateUser = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => apiClient.updateUser(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
};

export const useDeleteUser = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => apiClient.deleteUser(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
};

// Customers
export const useCustomers = (skip = 0, limit = 100, name?: string) => {
  return useQuery({
    queryKey: ['customers', skip, limit, name],
    queryFn: () => apiClient.getCustomers(skip, limit, name),
    select: (response) => response.data,
  });
};

export const useCustomer = (id: number) => {
  return useQuery({
    queryKey: ['customers', id],
    queryFn: () => apiClient.getCustomer(id),
    select: (response) => response.data,
  });
};

export const useCreateCustomer = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: any) => apiClient.createCustomer(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['customers'] });
    },
  });
};

export const useUpdateCustomer = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) =>
      apiClient.updateCustomer(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['customers'] });
    },
  });
};

export const useDeleteCustomer = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => apiClient.deleteCustomer(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['customers'] });
    },
  });
};

// Ingredients
export const useIngredients = (skip = 0, limit = 100, activeOnly = false) => {
  return useQuery({
    queryKey: ['ingredients', skip, limit, activeOnly],
    queryFn: () => apiClient.getIngredients(skip, limit, activeOnly),
    select: (response) => response.data,
  });
};

export const useLowStockIngredients = () => {
  return useQuery({
    queryKey: ['ingredients', 'low-stock'],
    queryFn: () => apiClient.getLowStockIngredients(),
    select: (response) => response.data,
  });
};

export const useIngredient = (id: number) => {
  return useQuery({
    queryKey: ['ingredients', id],
    queryFn: () => apiClient.getIngredient(id),
    select: (response) => response.data,
  });
};

export const useCreateIngredient = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: any) => apiClient.createIngredient(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ingredients'] });
    },
  });
};

export const useUpdateIngredient = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) =>
      apiClient.updateIngredient(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ingredients'] });
    },
  });
};

export const useDeleteIngredient = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => apiClient.deleteIngredient(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ingredients'] });
    },
  });
};

export const useIngredientTransactions = (ingredientId: number, skip = 0, limit = 100) => {
  return useQuery({
    queryKey: ['ingredients', ingredientId, 'transactions', skip, limit],
    queryFn: () => apiClient.getIngredientTransactions(ingredientId, skip, limit),
    select: (response) => response.data,
  });
};

export const useCreateIngredientTransaction = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ ingredientId, data }: { ingredientId: number; data: any }) =>
      apiClient.createIngredientTransaction(ingredientId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ingredients'] });
    },
  });
};

// Recipes
export const useRecipes = (skip = 0, limit = 100, category?: string, activeOnly = false) => {
  return useQuery({
    queryKey: ['recipes', skip, limit, category, activeOnly],
    queryFn: () => apiClient.getRecipes(skip, limit, category, activeOnly),
    select: (response) => response.data,
  });
};

export const useRecipe = (id: number) => {
  return useQuery({
    queryKey: ['recipes', id],
    queryFn: () => apiClient.getRecipe(id),
    select: (response) => response.data,
  });
};

export const useCreateRecipe = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: any) => apiClient.createRecipe(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['recipes'] });
    },
  });
};

export const useUpdateRecipe = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => apiClient.updateRecipe(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['recipes'] });
    },
  });
};

export const useDeleteRecipe = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => apiClient.deleteRecipe(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['recipes'] });
    },
  });
};

// Recipe Variants
export const useRecipeVariants = (recipeId: number) => {
  return useQuery({
    queryKey: ['recipes', recipeId, 'variants'],
    queryFn: () => apiClient.getRecipeVariants(recipeId),
    select: (response) => response.data,
  });
};

export const useRecipeVariant = (variantId: number) => {
  return useQuery({
    queryKey: ['recipe-variants', variantId],
    queryFn: () => apiClient.getRecipeVariant(variantId),
    select: (response) => response.data,
  });
};

export const useCreateRecipeVariant = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ recipeId, data }: { recipeId: number; data: any }) =>
      apiClient.createRecipeVariant(recipeId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['recipes'] });
    },
  });
};

// Orders
export const useOrders = (skip = 0, limit = 100, customerId?: number, status?: string) => {
  return useQuery({
    queryKey: ['orders', skip, limit, customerId, status],
    queryFn: () => apiClient.getOrders(skip, limit, customerId, status),
    select: (response) => response.data,
  });
};

export const useUpcomingDeliveries = () => {
  return useQuery({
    queryKey: ['orders', 'upcoming-deliveries'],
    queryFn: () => apiClient.getUpcomingDeliveries(),
    select: (response) => response.data,
  });
};

export const useOrder = (id: number) => {
  return useQuery({
    queryKey: ['orders', id],
    queryFn: () => apiClient.getOrder(id),
    select: (response) => response.data,
  });
};

export const useCreateOrder = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: any) => apiClient.createOrder(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
    },
  });
};

export const useUpdateOrder = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => apiClient.updateOrder(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
    },
  });
};

export const useDeleteOrder = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => apiClient.deleteOrder(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
    },
  });
};

// Order Cost Summary
export const useOrderCostSummary = (orderId: number) => {
  return useQuery({
    queryKey: ['orders', orderId, 'cost-summary'],
    queryFn: () => apiClient.getOrderCostSummary(orderId),
    select: (response) => response.data,
  });
};
