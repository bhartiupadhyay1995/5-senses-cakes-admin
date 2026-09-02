import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Plus, Search, BookOpen, Clock, Users } from 'lucide-react';

interface Recipe {
  id: number;
  name: string;
  prep_time: number;
  bake_time: number;
  servings: number;
  ingredients_count: number;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  last_used?: string;
}

const mockRecipes: Recipe[] = [
  {
    id: 1,
    name: 'Chocolate Cake',
    prep_time: 30,
    bake_time: 35,
    servings: 12,
    ingredients_count: 8,
    difficulty: 'Easy',
    last_used: '2 days ago',
  },
  {
    id: 2,
    name: 'Vanilla Cheesecake',
    prep_time: 45,
    bake_time: 60,
    servings: 8,
    ingredients_count: 12,
    difficulty: 'Medium',
    last_used: '5 days ago',
  },
  {
    id: 3,
    name: 'Red Velvet Cake',
    prep_time: 40,
    bake_time: 30,
    servings: 10,
    ingredients_count: 10,
    difficulty: 'Medium',
    last_used: '1 week ago',
  },
];

export const RecipesPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRecipe, setSelectedRecipe] = useState<Recipe | null>(null);

  const filteredRecipes = mockRecipes.filter((recipe) =>
    recipe.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'Easy':
        return 'bg-emerald-50 text-emerald-700 border-emerald-100';
      case 'Medium':
        return 'bg-amber-50 text-amber-700 border-amber-100';
      case 'Hard':
        return 'bg-rose-50 text-rose-700 border-rose-100';
      default:
        return 'bg-slate-50 text-slate-700 border-slate-100';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="rounded-3xl bg-gradient-to-r from-violet-500 via-purple-500 to-pink-400 p-6 text-white shadow-lg shadow-purple-200/60">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <div className="mb-2 inline-flex items-center gap-2 rounded-full bg-white/15 px-3 py-1 text-xs font-semibold tracking-wide uppercase text-purple-50">
              <BookOpen className="h-3.5 w-3.5" />
              Recipe library
            </div>
            <h1 className="text-3xl font-bold tracking-tight">Recipes</h1>
            <p className="mt-2 max-w-xl text-sm text-purple-50/90">Manage your cake recipes and create new flavor combinations.</p>
          </div>
          <Button className="w-full bg-white text-purple-600 hover:bg-purple-50 md:w-auto">
            <Plus className="mr-2 h-4 w-4" />
            New Recipe
          </Button>
        </div>
      </div>

      {/* Search Bar */}
      <Card className="border-purple-100">
        <CardContent className="pt-6">
          <div className="relative">
            <Search className="absolute left-3 top-3 h-5 w-5 text-slate-400" />
            <input
              type="text"
              placeholder="Search recipes..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full rounded-lg border border-slate-200 bg-white py-2 pl-10 pr-4 text-sm focus:border-purple-500 focus:outline-none focus:ring-1 focus:ring-purple-500"
            />
          </div>
        </CardContent>
      </Card>

      {/* Recipes Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {filteredRecipes.map((recipe) => (
          <Card
            key={recipe.id}
            className="cursor-pointer border-purple-100 transition-all hover:shadow-lg hover:shadow-purple-100/50"
            onClick={() => setSelectedRecipe(recipe)}
          >
            <CardHeader>
              <CardTitle className="text-lg">{recipe.name}</CardTitle>
              <div className="mt-2 flex gap-2">
                <span className={`inline-flex rounded-full px-2 py-1 text-xs font-semibold border ${getDifficultyColor(recipe.difficulty)}`}>
                  {recipe.difficulty}
                </span>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center gap-3 rounded-lg bg-slate-50 p-3">
                  <Clock className="h-4 w-4 text-purple-600" />
                  <div>
                    <p className="text-xs text-slate-500">Total time</p>
                    <p className="font-semibold text-slate-900">{recipe.prep_time + recipe.bake_time} min</p>
                  </div>
                </div>
                <div className="flex items-center gap-3 rounded-lg bg-slate-50 p-3">
                  <Users className="h-4 w-4 text-purple-600" />
                  <div>
                    <p className="text-xs text-slate-500">Servings</p>
                    <p className="font-semibold text-slate-900">{recipe.servings} servings</p>
                  </div>
                </div>
                <div className="text-sm text-slate-600">
                  <p>{recipe.ingredients_count} ingredients</p>
                  {recipe.last_used && <p className="text-xs text-slate-500">Last used: {recipe.last_used}</p>}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Recipe Detail Panel */}
      {selectedRecipe && (
        <Card className="border-purple-100 bg-gradient-to-br from-white to-purple-50/70">
          <CardHeader>
            <div className="flex items-start justify-between">
              <div>
                <CardTitle>{selectedRecipe.name}</CardTitle>
                <CardDescription>Full recipe details</CardDescription>
              </div>
              <button
                onClick={() => setSelectedRecipe(null)}
                className="text-slate-400 hover:text-slate-600"
              >
                ✕
              </button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-3">
                <div>
                  <p className="text-sm text-slate-600">Prep Time</p>
                  <p className="text-xl font-semibold text-slate-900">{selectedRecipe.prep_time} minutes</p>
                </div>
                <div>
                  <p className="text-sm text-slate-600">Bake Time</p>
                  <p className="text-xl font-semibold text-slate-900">{selectedRecipe.bake_time} minutes</p>
                </div>
              </div>
              <div className="space-y-3">
                <div>
                  <p className="text-sm text-slate-600">Servings</p>
                  <p className="text-xl font-semibold text-slate-900">{selectedRecipe.servings}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-600">Ingredients</p>
                  <p className="text-xl font-semibold text-slate-900">{selectedRecipe.ingredients_count} items</p>
                </div>
              </div>
            </div>
            <div className="mt-4 flex gap-2">
              <Button className="bg-purple-600 hover:bg-purple-700">Edit Recipe</Button>
              <Button variant="ghost">Duplicate</Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};
