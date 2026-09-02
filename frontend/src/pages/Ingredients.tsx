import React, { useState } from 'react';
import { useIngredients, useCreateIngredient, useDeleteIngredient } from '../hooks/useApi';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Label } from '../components/ui/Label';
import { Plus, Trash2, Edit2 } from 'lucide-react';
import { formatCurrency, formatQuantity } from '../utils/formatters';

export const IngredientsPage: React.FC = () => {
  const [activeOnly, setActiveOnly] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    category: '',
    base_unit: '',
    current_cost_per_unit: 0,
    current_quantity: 0,
    min_threshold: 0,
    supplier: '',
    active: true,
  });

  const { data: ingredients = [], isLoading } = useIngredients(0, 100, activeOnly);
  const createMutation = useCreateIngredient();
  const deleteMutation = useDeleteIngredient();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createMutation.mutate(formData, {
      onSuccess: () => {
        setFormData({
          name: '',
          category: '',
          base_unit: '',
          current_cost_per_unit: 0,
          current_quantity: 0,
          min_threshold: 0,
          supplier: '',
          active: true,
        });
        setShowForm(false);
      },
    });
  };

  const handleDelete = (id: number) => {
    if (window.confirm('Are you sure you want to delete this ingredient?')) {
      deleteMutation.mutate(id);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Ingredients</h1>
          <p className="text-gray-600">Manage your ingredient inventory</p>
        </div>
        <Button onClick={() => setShowForm(!showForm)}>
          <Plus className="mr-2 h-4 w-4" />
          Add Ingredient
        </Button>
      </div>

      {showForm && (
        <Card>
          <CardHeader>
            <CardTitle>New Ingredient</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <Label htmlFor="name">Name</Label>
                  <Input
                    id="name"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="category">Category</Label>
                  <Input
                    id="category"
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  />
                </div>
                <div>
                  <Label htmlFor="base_unit">Unit</Label>
                  <Input
                    id="base_unit"
                    value={formData.base_unit}
                    onChange={(e) => setFormData({ ...formData, base_unit: e.target.value })}
                  />
                </div>
                <div>
                  <Label htmlFor="cost">Cost per Unit</Label>
                  <Input
                    id="cost"
                    type="number"
                    step="0.01"
                    value={formData.current_cost_per_unit}
                    onChange={(e) =>
                      setFormData({ ...formData, current_cost_per_unit: parseFloat(e.target.value) })
                    }
                  />
                </div>
                <div>
                  <Label htmlFor="quantity">Current Quantity</Label>
                  <Input
                    id="quantity"
                    type="number"
                    value={formData.current_quantity}
                    onChange={(e) =>
                      setFormData({ ...formData, current_quantity: parseFloat(e.target.value) })
                    }
                  />
                </div>
                <div>
                  <Label htmlFor="min_threshold">Min Threshold</Label>
                  <Input
                    id="min_threshold"
                    type="number"
                    value={formData.min_threshold}
                    onChange={(e) =>
                      setFormData({ ...formData, min_threshold: parseFloat(e.target.value) })
                    }
                  />
                </div>
                <div>
                  <Label htmlFor="supplier">Supplier</Label>
                  <Input
                    id="supplier"
                    value={formData.supplier}
                    onChange={(e) => setFormData({ ...formData, supplier: e.target.value })}
                  />
                </div>
              </div>
              <div className="flex space-x-2">
                <Button type="submit" disabled={createMutation.isPending}>
                  {createMutation.isPending ? 'Creating...' : 'Create Ingredient'}
                </Button>
                <Button variant="outline" onClick={() => setShowForm(false)}>
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      <div className="flex items-center space-x-2">
        <input
          type="checkbox"
          id="active-only"
          checked={activeOnly}
          onChange={(e) => setActiveOnly(e.target.checked)}
          className="rounded"
        />
        <Label htmlFor="active-only">Active only</Label>
      </div>

      {isLoading ? (
        <div className="text-center text-gray-500">Loading ingredients...</div>
      ) : ingredients && ingredients.length > 0 ? (
        <div className="grid gap-4">
          {ingredients.map((ingredient: any) => (
            <Card key={ingredient.id}>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h3 className="font-semibold">{ingredient.name}</h3>
                    <p className="text-sm text-gray-600">
                      {ingredient.category} • {ingredient.supplier}
                    </p>
                    <div className="mt-2 grid gap-2 md:grid-cols-3">
                      <div>
                        <p className="text-xs text-gray-500">Cost per Unit</p>
                        <p className="text-sm font-medium">{formatCurrency(ingredient.current_cost_per_unit)}</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500">Current Stock</p>
                        <p className="text-sm font-medium">
                          {formatQuantity(ingredient.current_quantity, ingredient.base_unit)}
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500">Min Threshold</p>
                        <p className="text-sm font-medium">
                          {formatQuantity(ingredient.min_threshold, ingredient.base_unit)}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <Button variant="outline" size="icon">
                      <Edit2 className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="destructive"
                      size="icon"
                      onClick={() => handleDelete(ingredient.id)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="pt-6 text-center text-gray-500">
            No ingredients found
          </CardContent>
        </Card>
      )}
    </div>
  );
};
