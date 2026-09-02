import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Package,
  BookOpen,
  ShoppingCart,
  DollarSign,
  Settings,
  ChevronDown,
  Menu,
  X,
} from 'lucide-react';
import { Button } from '../ui/Button';
import { cn } from '../../utils/cn';

interface NavItem {
  name: string;
  href?: string;
  icon?: React.ReactNode;
  children?: NavItem[];
}

const navItems: NavItem[] = [
  {
    name: 'Dashboard',
    href: '/',
    icon: <LayoutDashboard className="h-5 w-5" />,
  },
  {
    name: 'Inventory',
    icon: <Package className="h-5 w-5" />,
    children: [
      { name: 'Ingredients', href: '/inventory/ingredients', icon: null },
      { name: 'Supplies', href: '/inventory/supplies', icon: null },
      { name: 'Low Stock', href: '/inventory/low-stock', icon: null },
    ],
  },
  {
    name: 'Recipes',
    href: '/recipes',
    icon: <BookOpen className="h-5 w-5" />,
  },
  {
    name: 'Orders',
    icon: <ShoppingCart className="h-5 w-5" />,
    children: [
      { name: 'All Orders', href: '/orders', icon: null },
      { name: 'Upcoming Deliveries', href: '/orders/upcoming', icon: null },
      { name: 'New Order', href: '/orders/new', icon: null },
    ],
  },
  {
    name: 'Profitability',
    icon: <DollarSign className="h-5 w-5" />,
    children: [
      { name: 'Analysis', href: '/profitability/analysis', icon: null },
      { name: 'Reports', href: '/profitability/reports', icon: null },
    ],
  },
  {
    name: 'Settings',
    href: '/settings',
    icon: <Settings className="h-5 w-5" />,
  },
];

export const Sidebar: React.FC = () => {
  const location = useLocation();
  const [open, setOpen] = useState(false);
  const [expandedItems, setExpandedItems] = useState<string[]>([]);

  const toggleExpand = (name: string) => {
    setExpandedItems((prev) =>
      prev.includes(name) ? prev.filter((item) => item !== name) : [...prev, name]
    );
  };

  const NavLink: React.FC<NavItem & { isChild?: boolean }> = ({
    name,
    href,
    icon,
    children,
    isChild,
  }) => {
    const isActive = href && location.pathname === href;
    const hasChildren = children && children.length > 0;
    const isExpanded = expandedItems.includes(name);

    return (
      <div>
        {href ? (
          <Link
            to={href}
            className={cn(
              'flex items-center space-x-3 rounded-md px-3 py-2 text-sm font-medium transition-colors',
              isActive
                ? 'bg-slate-100 text-slate-900'
                : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900',
              isChild && 'pl-11'
            )}
          >
            {icon}
            <span>{name}</span>
          </Link>
        ) : (
          <button
            onClick={() => hasChildren && toggleExpand(name)}
            className={cn(
              'flex w-full items-center justify-between rounded-md px-3 py-2 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-50 hover:text-slate-900',
              isExpanded && 'bg-slate-50'
            )}
          >
            <div className="flex items-center space-x-3">
              {icon}
              <span>{name}</span>
            </div>
            {hasChildren && (
              <ChevronDown
                className={cn('h-4 w-4 transition-transform', isExpanded && 'rotate-180')}
              />
            )}
          </button>
        )}
        {hasChildren && isExpanded && (
          <div className="space-y-1 py-1">
            {children.map((child) => (
              <NavLink key={child.name} {...child} isChild />
            ))}
          </div>
        )}
      </div>
    );
  };

  return (
    <>
      {/* Mobile menu button */}
      <div className="flex items-center justify-between border-b border-slate-200 px-4 py-4 md:hidden">
        <h1 className="text-xl font-bold">5 Senses Cakes</h1>
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setOpen(!open)}
        >
          {open ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </Button>
      </div>

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed inset-y-0 left-0 z-50 w-64 border-r border-slate-200 bg-white pt-20 md:static md:z-auto md:pt-0',
          !open && 'hidden md:block'
        )}
      >
        <div className="hidden px-4 py-6 md:block">
          <h1 className="text-xl font-bold">5 Senses Cakes</h1>
        </div>
        <nav className="space-y-1 px-4 py-4">
          {navItems.map((item) => (
            <NavLink key={item.name} {...item} />
          ))}
        </nav>
      </aside>

      {/* Mobile overlay */}
      {open && (
        <div
          className="fixed inset-0 z-40 bg-black bg-opacity-50 md:hidden"
          onClick={() => setOpen(false)}
        />
      )}
    </>
  );
};
