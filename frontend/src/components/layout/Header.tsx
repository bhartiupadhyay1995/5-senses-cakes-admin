import React from 'react';
import { Bell, User, LogOut } from 'lucide-react';
import { Button } from '../ui/Button';

export const Header: React.FC = () => {
  return (
    <header className="sticky top-0 z-40 border-b border-slate-200 bg-white">
      <div className="flex items-center justify-between px-4 py-4 md:px-6">
        <div className="flex items-center space-x-4">
          <h2 className="text-lg font-semibold text-slate-900 md:hidden">5 Senses Cakes</h2>
        </div>
        <div className="flex items-center space-x-4">
          <Button variant="ghost" size="icon">
            <Bell className="h-5 w-5" />
          </Button>
          <Button variant="ghost" size="icon">
            <User className="h-5 w-5" />
          </Button>
          <Button variant="ghost" size="icon">
            <LogOut className="h-5 w-5" />
          </Button>
        </div>
      </div>
    </header>
  );
};
