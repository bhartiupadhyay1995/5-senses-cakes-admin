# Frontend — React + TypeScript Application

A modern, responsive web UI for managing 5 Senses Cakes business.

## Stack

- React 18
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui
- React Router
- TanStack Query (React Query)
- Recharts
- Playwright (E2E testing)

## Setup

### Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

### Build

```bash
# Production build
npm run build

# Preview production build
npm run preview
```

### Testing

```bash
# Run Playwright E2E tests
npm run test:e2e

# Run tests in headed mode
npm run test:e2e:headed
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Navigation.tsx
│   │   │   ├── DataTable.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── LoadingSpinner.tsx
│   │   ├── forms/
│   │   │   ├── IngredientForm.tsx
│   │   │   ├── RecipeForm.tsx
│   │   │   ├── OrderForm.tsx
│   │   │   └── CustomerForm.tsx
│   │   ├── dashboard/
│   │   │   ├── DashboardCard.tsx
│   │   │   ├── SummaryMetrics.tsx
│   │   │   ├── ChartCard.tsx
│   │   │   └── LowStockAlert.tsx
│   │   ├── inventory/
│   │   │   ├── IngredientsList.tsx
│   │   │   ├── SuppliesList.tsx
│   │   │   ├── TransactionHistory.tsx
│   │   │   └── PurchaseForm.tsx
│   │   ├── recipes/
│   │   │   ├── RecipesList.tsx
│   │   │   ├── RecipeDetail.tsx
│   │   │   ├── VariantManager.tsx
│   │   │   └── CostCalculator.tsx
│   │   ├── orders/
│   │   │   ├── OrdersList.tsx
│   │   │   ├── OrderDetail.tsx
│   │   │   ├── OrderForm.tsx
│   │   │   ├── CostBreakdown.tsx
│   │   │   ├── LaborEntry.tsx
│   │   │   └── ProfitabilitySummary.tsx
│   │   ├── analytics/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Charts.tsx
│   │   │   ├── FilterPanel.tsx
│   │   │   ├── ProfitabilityView.tsx
│   │   │   ├── CustomerAnalytics.tsx
│   │   │   └── InventoryAnalytics.tsx
│   │   └── settings/
│   │       ├── SettingsPage.tsx
│   │       ├── LaborRateForm.tsx
│   │       └── OperatingCostsForm.tsx
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── Inventory.tsx
│   │   ├── Recipes.tsx
│   │   ├── Orders.tsx
│   │   ├── Analytics.tsx
│   │   ├── Settings.tsx
│   │   └── NotFound.tsx
│   ├── services/
│   │   ├── api.ts              # Axios/fetch configuration
│   │   ├── ingredientService.ts
│   │   ├── recipeService.ts
│   │   ├── orderService.ts
│   │   ├── customerService.ts
│   │   └── analyticsService.ts
│   ├── hooks/
│   │   ├── useIngredients.ts
│   │   ├── useRecipes.ts
│   │   ├── useOrders.ts
│   │   ├── usePagination.ts
│   │   ├── useFilter.ts
│   │   └── useDebounce.ts
│   ├── types/
│   │   ├── index.ts            # Type definitions
│   │   ├── api.ts              # API response types
│   │   └── forms.ts            # Form types
│   ├── utils/
│   │   ├── formatting.ts       # Formatting helpers
│   │   ├── calculations.ts     # Calculation helpers
│   │   └── validation.ts       # Form validation
│   ├── context/
│   │   └── AppContext.tsx      # Global state (optional)
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css               # Global styles
├── public/
│   ├── favicon.svg
│   └── logo.png
├── tests/
│   ├── e2e/
│   │   ├── dashboard.spec.ts
│   │   ├── ingredients.spec.ts
│   │   ├── recipes.spec.ts
│   │   ├── orders.spec.ts
│   │   └── analytics.spec.ts
│   └── fixtures/
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
├── playwright.config.ts
├── .env.example
├── Dockerfile
└── README.md
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
VITE_API_URL=http://localhost:8000/api
```

## Key Features

- **Dashboard**: Real-time business metrics and KPIs
- **Inventory Management**: Track ingredients and supplies
- **Recipe Management**: Create, edit, and cost recipes
- **Order Management**: Complete order lifecycle
- **Analytics**: Revenue, profit, and customer analysis
- **Responsive Design**: Works on desktop, tablet, and mobile

## Styling

Uses Tailwind CSS with shadcn/ui component library for consistency and accessibility.

- Global styles in `index.css`
- Component-specific styles using Tailwind utility classes
- Dark mode support (can be configured in `tailwind.config.js`)

## API Integration

All API calls go through the services layer in `src/services/`.  
Uses TanStack Query for caching and state management.

## Deployment

### Docker

```bash
docker build -t 5-senses-cakes-frontend .
docker run -p 5173:5173 --env-file .env 5-senses-cakes-frontend
```

