import React, { useState } from 'react';
import { useUpcomingDeliveries } from '../hooks/useApi';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { formatDate, formatCurrency, formatOrderStatus, getStatusColor } from '../utils/formatters';
import { TrendingUp, Package, ShoppingCart, AlertCircle, Sparkles, CakeSlice } from 'lucide-react';

const tabs = ['Overview', 'Orders', 'Inventory', 'Profitability'];

export const Dashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState('Overview');
  const { data: upcomingDeliveries, isLoading } = useUpcomingDeliveries();

  const stats = [
    {
      title: 'Total Revenue',
      value: '$12,450',
      change: '+5.2%',
      icon: <TrendingUp className="h-8 w-8 text-emerald-600" />,
      tone: 'bg-emerald-50 border-emerald-100',
    },
    {
      title: 'Pending Orders',
      value: '8',
      change: '+2 this week',
      icon: <ShoppingCart className="h-8 w-8 text-blue-600" />,
      tone: 'bg-blue-50 border-blue-100',
    },
    {
      title: 'Low Stock Items',
      value: '3',
      change: 'Urgent',
      icon: <AlertCircle className="h-8 w-8 text-rose-600" />,
      tone: 'bg-rose-50 border-rose-100',
    },
    {
      title: 'Profit Margin',
      value: '38.5%',
      change: '+2.1%',
      icon: <Package className="h-8 w-8 text-violet-600" />,
      tone: 'bg-violet-50 border-violet-100',
    },
  ];

  const quickActions = [
    { label: 'This Month\'s Revenue', value: '$3,240', color: 'bg-pink-50 text-pink-700' },
    { label: 'Average Order Value', value: '$405', color: 'bg-amber-50 text-amber-700' },
    { label: 'Total Orders', value: '8', color: 'bg-cyan-50 text-cyan-700' },
    { label: 'Completion Rate', value: '100%', color: 'bg-emerald-50 text-emerald-700' },
  ];

  const orderRows = upcomingDeliveries?.slice(0, 4) ?? [];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'Orders':
        return (
          <Card className="border-rose-100 bg-gradient-to-br from-white to-rose-50/50">
            <CardHeader>
              <CardTitle>Order Pipeline</CardTitle>
              <CardDescription>Current order stages and delivery timeline</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {orderRows.length > 0 ? orderRows.map((order: any) => (
                  <div key={order.id} className="flex items-center justify-between rounded-xl border border-rose-100 bg-white p-3">
                    <div>
                      <p className="font-semibold text-slate-800">Order #{order.id}</p>
                      <p className="text-sm text-slate-500">Due {formatDate(order.delivery_date)}</p>
                    </div>
                    <div className="text-right">
                      <span className={`inline-flex rounded-full px-2.5 py-1 text-xs font-semibold ${getStatusColor(order.status)}`}>
                        {formatOrderStatus(order.status)}
                      </span>
                      <p className="mt-1 text-sm font-semibold text-slate-700">{formatCurrency(order.selling_price)}</p>
                    </div>
                  </div>
                )) : (
                  <div className="text-center text-slate-500">No upcoming deliveries</div>
                )}
              </div>
            </CardContent>
          </Card>
        );
      case 'Inventory':
        return (
          <Card className="border-cyan-100 bg-gradient-to-br from-white to-cyan-50/60">
            <CardHeader>
              <CardTitle>Inventory Focus</CardTitle>
              <CardDescription>Stock status and ingredient readiness</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-3">
                <div className="rounded-xl bg-cyan-50 p-4">
                  <p className="text-sm text-cyan-700">Low stock</p>
                  <p className="mt-2 text-2xl font-bold text-cyan-900">3 items</p>
                </div>
                <div className="rounded-xl bg-amber-50 p-4">
                  <p className="text-sm text-amber-700">Top supplier</p>
                  <p className="mt-2 text-2xl font-bold text-amber-900">Fresh Foods</p>
                </div>
                <div className="rounded-xl bg-emerald-50 p-4">
                  <p className="text-sm text-emerald-700">Stock health</p>
                  <p className="mt-2 text-2xl font-bold text-emerald-900">92%</p>
                </div>
              </div>
            </CardContent>
          </Card>
        );
      case 'Profitability':
        return (
          <Card className="border-violet-100 bg-gradient-to-br from-white to-violet-50/70">
            <CardHeader>
              <CardTitle>Profitability Snapshot</CardTitle>
              <CardDescription>Margin trends and cost efficiency</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2">
                <div className="rounded-xl bg-violet-50 p-4">
                  <p className="text-sm text-violet-700">Gross margin</p>
                  <p className="mt-2 text-2xl font-bold text-violet-900">42.6%</p>
                </div>
                <div className="rounded-xl bg-pink-50 p-4">
                  <p className="text-sm text-pink-700">Labor efficiency</p>
                  <p className="mt-2 text-2xl font-bold text-pink-900">91%</p>
                </div>
              </div>
            </CardContent>
          </Card>
        );
      default:
        return (
          <>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              {stats.map((stat) => (
                <Card key={stat.title} className={`${stat.tone} border`}> 
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium text-slate-700">{stat.title}</CardTitle>
                    <div className="rounded-lg bg-white/80 p-2 shadow-sm">{stat.icon}</div>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-slate-900">{stat.value}</div>
                    <p className="text-xs font-medium text-slate-600">{stat.change}</p>
                  </CardContent>
                </Card>
              ))}
            </div>

            <Card className="border-pink-100 bg-gradient-to-br from-white to-pink-50/70">
              <CardHeader>
                <CardTitle>Upcoming Deliveries</CardTitle>
                <CardDescription>Orders that need to be completed this week</CardDescription>
              </CardHeader>
              <CardContent>
                {isLoading ? (
                  <div className="text-center text-slate-500">Loading...</div>
                ) : orderRows.length > 0 ? (
                  <div className="space-y-4">
                    {orderRows.map((order: any) => (
                      <div key={order.id} className="flex items-center justify-between border-b border-slate-200 pb-4 last:border-0 last:pb-0">
                        <div>
                          <p className="font-semibold text-slate-800">Order #{order.id}</p>
                          <p className="text-sm text-slate-500">Customer: {order.customer_id} • Due: {formatDate(order.delivery_date)}</p>
                        </div>
                        <div className="text-right">
                          <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${getStatusColor(order.status)}`}>
                            {formatOrderStatus(order.status)}
                          </span>
                          <p className="mt-1 text-sm font-semibold text-slate-700">{formatCurrency(order.selling_price)}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center text-slate-500">No upcoming deliveries</div>
                )}
              </CardContent>
            </Card>
            <Card className="border-slate-200 bg-white">
              <CardHeader>
                <CardTitle>Quick Stats</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
                  {quickActions.map((item) => (
                    <div key={item.label} className={`rounded-2xl p-4 ${item.color}`}>
                      <p className="text-sm font-medium">{item.label}</p>
                      <p className="mt-2 text-2xl font-bold">{item.value}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </>
        );
    }
  };

  return (
    <div className="space-y-6">
      <div className="rounded-3xl bg-gradient-to-r from-pink-500 via-rose-500 to-orange-400 p-6 text-white shadow-lg shadow-pink-200/60">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <div className="mb-2 inline-flex items-center gap-2 rounded-full bg-white/15 px-3 py-1 text-xs font-semibold tracking-wide uppercase text-pink-50">
              <Sparkles className="h-3.5 w-3.5" />
              Business overview
            </div>
            <h1 className="text-3xl font-bold tracking-tight">5 Senses Cakes</h1>
            <p className="mt-2 max-w-xl text-sm text-pink-50/90">Track orders, manage inventory, and keep the business moving smoothly from quote to delivery.</p>
          </div>
          <div className="flex items-center gap-3 rounded-2xl bg-white/10 px-4 py-3 backdrop-blur-sm">
            <CakeSlice className="h-8 w-8 text-pink-100" />
            <div>
              <p className="text-xs uppercase tracking-[0.2em] text-pink-100/80">Today</p>
              <p className="text-lg font-semibold">4 active orders</p>
            </div>
          </div>
        </div>
      </div>

      <div className="rounded-2xl border border-pink-100 bg-white p-2 shadow-sm">
        <div className="flex flex-wrap gap-2">
          {tabs.map((tab) => (
            <Button
              key={tab}
              variant={activeTab === tab ? 'default' : 'ghost'}
              className={activeTab === tab ? 'bg-gradient-to-r from-rose-500 to-pink-500 text-white hover:from-rose-600 hover:to-pink-600' : 'text-slate-600 hover:bg-pink-50 hover:text-rose-600'}
              onClick={() => setActiveTab(tab)}
            >
              {tab}
            </Button>
          ))}
        </div>
      </div>

      {renderTabContent()}
    </div>
  );
};
