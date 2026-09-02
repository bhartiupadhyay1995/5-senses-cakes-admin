# 5 Senses Cakes Frontend - Quick Start Guide

## Phase 4 Implementation: Frontend UI

### ✅ What's Been Built

#### Frontend Architecture
- **React 18** with TypeScript and Vite
- **TailwindCSS** for responsive styling
- **React Router** for navigation
- **TanStack React Query** for data fetching and caching
- **Radix UI** for accessible components
- **Lucide Icons** for consistent iconography

#### API Integration
- Complete API client with all 80+ endpoints
- Custom React Query hooks for all entities
- Automatic cache invalidation
- Error handling and loading states

#### UI Components (5 core components)
- **Button** - Multiple variants and sizes
- **Card** - Container with header, content, footer
- **Input** - Text input field
- **Label** - Form label
- **Textarea** - Multi-line text input

#### Layout Components
- **Sidebar** - Collapsible navigation with nested menus
- **Header** - Top navigation bar
- **MainLayout** - Responsive layout wrapper

#### Pages (2 complete pages)
- **Dashboard** - Overview with stats and upcoming deliveries
- **Ingredients** - Inventory management with CRUD operations

#### Utility Functions
- Date and time formatting
- Currency and number formatting
- Order status display and colors
- Profit calculation helpers

---

## Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── client.ts              # API client with all endpoints
│   ├── components/
│   │   ├── layout/
│   │   │   ├── MainLayout.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Header.tsx
│   │   └── ui/
│   │       ├── Button.tsx
│   │       ├── Card.tsx
│   │       ├── Input.tsx
│   │       ├── Label.tsx
│   │       └── Textarea.tsx
│   ├── hooks/
│   │   └── useApi.ts              # React Query hooks
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   └── Ingredients.tsx
│   ├── types/
│   │   └── index.ts               # TypeScript interfaces
│   ├── utils/
│   │   ├── cn.ts
│   │   └── formatters.ts
│   ├── App.tsx                    # Main app component
│   ├── main.tsx                   # Entry point
│   └── index.css                  # Global styles
├── index.html
├── .env
├── vite.config.ts
├── tsconfig.json
└── tailwind.config.js
```

---

## Prerequisites

- Node.js 16 or higher
- npm or yarn
- Backend running at http://localhost:8000

---

## Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

The `.env` file is already configured to point to the backend API:
```
VITE_API_URL=http://localhost:8000/api/v1
```

Change this if your backend runs on a different address.

### 3. Start Development Server

```bash
npm run dev
```

The frontend will be available at: `http://localhost:5173`

### 4. Build for Production

```bash
npm run build
```

---

## Features Implemented

### Dashboard Page (`/`)
- **Key Metrics**: Revenue, Orders, Low Stock, Profit Margin
- **Upcoming Deliveries**: Real-time order status
- **Quick Stats**: Monthly revenue, average order value, completion rate

### Ingredients Page (`/inventory/ingredients`)
- **List View**: Display all ingredients with inventory levels
- **Create Ingredient**: Form to add new ingredients
- **Edit/Delete**: Modify or remove ingredients
- **Filters**: Active/inactive status toggle
- **Search**: Find ingredients by name

### Navigation
- **Main Sidebar**: Primary navigation with collapsible menus
  - Dashboard
  - Inventory (Ingredients, Supplies, Low Stock)
  - Recipes
  - Orders (All, Upcoming, New)
  - Profitability (Analysis, Reports)
  - Settings
- **Mobile Responsive**: Hamburger menu on mobile devices
- **Header**: User actions and notifications

---

## Available Routes

| Route | Page | Status |
|-------|------|--------|
| `/` | Dashboard | ✓ Implemented |
| `/inventory/ingredients` | Ingredients Management | ✓ Implemented |
| `/inventory/supplies` | Supplies Management | To Do |
| `/inventory/low-stock` | Low Stock Items | To Do |
| `/recipes` | Recipe Management | To Do |
| `/orders` | All Orders | To Do |
| `/orders/upcoming` | Upcoming Deliveries | To Do |
| `/orders/new` | Create New Order | To Do |
| `/profitability/analysis` | Profitability Analysis | To Do |
| `/profitability/reports` | Reports | To Do |
| `/settings` | Settings | To Do |

---

## Component Usage Examples

### Creating a New Page

```typescript
// pages/NewPage.tsx
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

export const NewPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Page Title</h1>
      <Card>
        <CardHeader>
          <CardTitle>Card Title</CardTitle>
        </CardHeader>
        <CardContent>
          <p>Your content here</p>
        </CardContent>
      </Card>
    </div>
  );
};
```

### Using API Hooks

```typescript
import { useIngredients, useCreateIngredient } from '../hooks/useApi';

function MyComponent() {
  const { data: ingredients, isLoading } = useIngredients(0, 100);
  const createMutation = useCreateIngredient();

  const handleCreate = (data: any) => {
    createMutation.mutate(data);
  };

  return (
    <div>
      {isLoading && <p>Loading...</p>}
      {ingredients?.map((item: any) => (
        <div key={item.id}>{item.name}</div>
      ))}
    </div>
  );
}
```

### Formatting Values

```typescript
import { formatCurrency, formatDate, formatOrderStatus } from '../utils/formatters';

// Use formatters
const price = formatCurrency(150.00);        // $150.00
const date = formatDate('2024-09-15');       // Sep 15, 2024
const status = formatOrderStatus('CONFIRMED'); // Confirmed
```

---

## Development Workflow

### 1. Create New Component

```bash
# Create in appropriate directory
src/components/ui/NewComponent.tsx
src/pages/NewPage.tsx
```

### 2. Add Types (if needed)

```typescript
// In src/types/index.ts
export interface NewEntity {
  id: number;
  name: string;
  // ... fields
}
```

### 3. Add API Endpoints (if needed)

```typescript
// In src/api/client.ts
getNewEntity(id: number) {
  return this.client.get(`/new-entities/${id}`);
}
```

### 4. Create Hooks

```typescript
// In src/hooks/useApi.ts
export const useNewEntity = (id: number) => {
  return useQuery({
    queryKey: ['new-entities', id],
    queryFn: () => apiClient.getNewEntity(id),
    select: (response) => response.data,
  });
};
```

### 5. Build Page

```typescript
// In src/pages/NewPage.tsx
import { useNewEntity } from '../hooks/useApi';

export const NewPage: React.FC = () => {
  const { data, isLoading } = useNewEntity(1);
  // ... render page
};
```

### 6. Add Route

```typescript
// In src/App.tsx
<Route path="/new-page" element={<NewPage />} />
```

---

## Styling Guide

All components use **TailwindCSS** classes. Common utilities:

```typescript
// Spacing
className="p-4"        // Padding
className="m-2"        // Margin
className="space-y-4"  // Vertical spacing

// Layout
className="flex"           // Flexbox
className="grid"           // CSS Grid
className="grid-cols-2"    // 2-column grid

// Responsive
className="md:grid-cols-2" // 2 columns on medium+ screens
className="lg:grid-cols-3" // 3 columns on large+ screens

// Colors
className="bg-blue-500"    // Blue background
className="text-red-600"   // Red text
className="border-gray-200" // Gray border

// Typography
className="text-lg"      // Large text
className="font-bold"    // Bold
className="text-center"  // Center aligned
```

---

## Testing Pages Locally

### Start Backend
```bash
# In backend directory
python -m uvicorn main:app --reload
```

### Start Frontend
```bash
# In frontend directory
npm run dev
```

### Access Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/v1
- API Docs: http://localhost:8000/docs

---

## Troubleshooting

### API Connection Error
```
Error: Cannot GET http://localhost:8000/api/v1/...
```
- Ensure backend is running
- Check .env VITE_API_URL matches backend address
- Check CORS is enabled in backend

### Module Import Errors
```
Module not found: 'src/components/...'
```
- Verify file exists in correct directory
- Check import path is correct
- Restart development server

### Styling Not Applied
- Ensure TailwindCSS classes are used (not custom CSS)
- Check tailwind.config.js includes src directory
- Restart dev server if config changed

---

## Next Steps for Phase 4

1. **Supplies Management** (`/inventory/supplies`)
   - Similar to ingredients page
   - Manage non-food items

2. **Recipe Management** (`/recipes`)
   - Create/edit recipes
   - Manage recipe variants
   - Add ingredients to recipes

3. **Order Management** (`/orders`)
   - View all orders
   - Create new orders
   - Track order status
   - Add components and costs

4. **Profitability Analysis** (`/profitability`)
   - Revenue vs cost charts
   - Profit margin analysis
   - Order profitability breakdown

5. **Settings** (`/settings`)
   - User profile
   - Business settings
   - Operating costs configuration

---

## Performance Optimizations

- **React Query** handles caching and automatic refetching
- **Lazy loading** for page components
- **Memoization** to prevent unnecessary re-renders
- **Virtualization** for large lists (future enhancement)

---

## Version

- **Phase 4 Version**: 0.1.0
- **Implementation Date**: September 2024
- **Status**: In Progress

---

## Support

For issues or questions:
- Check Backend API docs: http://localhost:8000/docs
- Review component examples in existing pages
- Consult TailwindCSS docs for styling: https://tailwindcss.com
