import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClientProvider, QueryClient } from '@tanstack/react-query';
import { MainLayout } from './components/layout/MainLayout';
import { Dashboard } from './pages/Dashboard';
import { IngredientsPage } from './pages/Ingredients';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <MainLayout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/inventory/ingredients" element={<IngredientsPage />} />
            {/* More routes will be added in subsequent phases */}
          </Routes>
        </MainLayout>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
