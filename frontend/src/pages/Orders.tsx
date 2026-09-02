import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Plus, Filter, Download, Calendar, DollarSign, User } from 'lucide-react';
import { formatDate, formatCurrency, formatOrderStatus, getStatusColor } from '../utils/formatters';

interface Order {
  id: number;
  customer_id: number;
  customer_name: string;
  order_date: string;
  delivery_date: string;
  selling_price: number;
  status: string;
  items_count: number;
}

const mockOrders: Order[] = [
  {
    id: 101,
    customer_id: 1,
    customer_name: 'Sarah Johnson',
    order_date: '2024-01-15',
    delivery_date: '2024-01-22',
    selling_price: 450,
    status: 'pending',
    items_count: 3,
  },
  {
    id: 102,
    customer_id: 2,
    customer_name: 'Mike Chen',
    order_date: '2024-01-16',
    delivery_date: '2024-01-23',
    selling_price: 550,
    status: 'in_progress',
    items_count: 2,
  },
  {
    id: 103,
    customer_id: 3,
    customer_name: 'Emma Davis',
    order_date: '2024-01-17',
    delivery_date: '2024-01-20',
    selling_price: 350,
    status: 'ready',
    items_count: 1,
  },
  {
    id: 104,
    customer_id: 4,
    customer_name: 'James Wilson',
    order_date: '2024-01-10',
    delivery_date: '2024-01-18',
    selling_price: 650,
    status: 'completed',
    items_count: 4,
  },
];

export const OrdersPage: React.FC = () => {
  const [filterStatus, setFilterStatus] = useState<string | null>(null);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);

  const filteredOrders = filterStatus
    ? mockOrders.filter((order) => order.status === filterStatus)
    : mockOrders;

  const stats = [
    {
      label: 'Total Orders',
      value: mockOrders.length.toString(),
      color: 'bg-blue-50 text-blue-700 border-blue-100',
    },
    {
      label: 'Pending',
      value: mockOrders.filter((o) => o.status === 'pending').length.toString(),
      color: 'bg-amber-50 text-amber-700 border-amber-100',
    },
    {
      label: 'In Progress',
      value: mockOrders.filter((o) => o.status === 'in_progress').length.toString(),
      color: 'bg-cyan-50 text-cyan-700 border-cyan-100',
    },
    {
      label: 'Ready',
      value: mockOrders.filter((o) => o.status === 'ready').length.toString(),
      color: 'bg-emerald-50 text-emerald-700 border-emerald-100',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="rounded-3xl bg-gradient-to-r from-blue-500 via-cyan-500 to-teal-400 p-6 text-white shadow-lg shadow-cyan-200/60">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <div className="mb-2 inline-flex items-center gap-2 rounded-full bg-white/15 px-3 py-1 text-xs font-semibold tracking-wide uppercase text-cyan-50">
              <Calendar className="h-3.5 w-3.5" />
              Order Management
            </div>
            <h1 className="text-3xl font-bold tracking-tight">Orders</h1>
            <p className="mt-2 max-w-xl text-sm text-cyan-50/90">Track and manage all customer orders from quote to delivery.</p>
          </div>
          <Button className="w-full bg-white text-cyan-600 hover:bg-cyan-50 md:w-auto">
            <Plus className="mr-2 h-4 w-4" />
            New Order
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.label} className={`border ${stat.color.split(' text-')[0]} ${stat.color.split('bg-')[1].split(' ')[0]}`}>
            <CardContent className="pt-6">
              <p className="text-sm font-medium text-slate-600">{stat.label}</p>
              <p className="mt-2 text-3xl font-bold text-slate-900">{stat.value}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Filter & Actions */}
      <Card className="border-cyan-100">
        <CardContent className="pt-6">
          <div className="flex flex-wrap gap-3">
            <Button
              variant={filterStatus === null ? 'default' : 'ghost'}
              onClick={() => setFilterStatus(null)}
              className={filterStatus === null ? 'bg-gradient-to-r from-cyan-500 to-teal-500 text-white' : ''}
            >
              All Orders
            </Button>
            <Button
              variant={filterStatus === 'pending' ? 'default' : 'ghost'}
              onClick={() => setFilterStatus('pending')}
              className={filterStatus === 'pending' ? 'bg-amber-500 text-white hover:bg-amber-600' : ''}
            >
              Pending
            </Button>
            <Button
              variant={filterStatus === 'in_progress' ? 'default' : 'ghost'}
              onClick={() => setFilterStatus('in_progress')}
              className={filterStatus === 'in_progress' ? 'bg-cyan-500 text-white hover:bg-cyan-600' : ''}
            >
              In Progress
            </Button>
            <Button
              variant={filterStatus === 'ready' ? 'default' : 'ghost'}
              onClick={() => setFilterStatus('ready')}
              className={filterStatus === 'ready' ? 'bg-emerald-500 text-white hover:bg-emerald-600' : ''}
            >
              Ready
            </Button>
            <Button variant="ghost" className="ml-auto">
              <Download className="mr-2 h-4 w-4" />
              Export
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Orders List */}
      <div className="space-y-3">
        {filteredOrders.map((order) => (
          <Card
            key={order.id}
            className="cursor-pointer border-cyan-100 bg-gradient-to-r from-white to-cyan-50/30 transition-all hover:shadow-md hover:shadow-cyan-100/50"
            onClick={() => setSelectedOrder(order)}
          >
            <CardContent className="pt-6">
              <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3">
                    <h3 className="text-lg font-semibold text-slate-900">Order #{order.id}</h3>
                    <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${getStatusColor(order.status)}`}>
                      {formatOrderStatus(order.status)}
                    </span>
                  </div>
                  <p className="mt-2 text-sm text-slate-600">
                    <User className="inline mr-1 h-4 w-4" />
                    {order.customer_name}
                  </p>
                  <div className="mt-2 flex flex-wrap gap-4 text-sm text-slate-600">
                    <span>Ordered: {formatDate(order.order_date)}</span>
                    <span>Due: {formatDate(order.delivery_date)}</span>
                    <span>{order.items_count} items</span>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm text-slate-600">Total</p>
                  <p className="text-2xl font-bold text-slate-900">{formatCurrency(order.selling_price)}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Order Detail Panel */}
      {selectedOrder && (
        <Card className="border-cyan-100 bg-gradient-to-br from-white to-cyan-50/70">
          <CardHeader>
            <div className="flex items-start justify-between">
              <div>
                <CardTitle>Order #{selectedOrder.id} Details</CardTitle>
                <CardDescription>Complete order information</CardDescription>
              </div>
              <button
                onClick={() => setSelectedOrder(null)}
                className="text-slate-400 hover:text-slate-600"
              >
                ✕
              </button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid gap-6 md:grid-cols-2">
              <div className="space-y-3">
                <div>
                  <p className="text-sm text-slate-600">Customer</p>
                  <p className="text-lg font-semibold text-slate-900">{selectedOrder.customer_name}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-600">Order Date</p>
                  <p className="text-lg font-semibold text-slate-900">{formatDate(selectedOrder.order_date)}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-600">Delivery Date</p>
                  <p className="text-lg font-semibold text-slate-900">{formatDate(selectedOrder.delivery_date)}</p>
                </div>
              </div>
              <div className="space-y-3">
                <div>
                  <p className="text-sm text-slate-600">Status</p>
                  <span className={`inline-flex rounded-full px-3 py-1 text-sm font-semibold ${getStatusColor(selectedOrder.status)}`}>
                    {formatOrderStatus(selectedOrder.status)}
                  </span>
                </div>
                <div>
                  <p className="text-sm text-slate-600">Items</p>
                  <p className="text-lg font-semibold text-slate-900">{selectedOrder.items_count} items</p>
                </div>
                <div>
                  <p className="text-sm text-slate-600">Total Price</p>
                  <p className="text-2xl font-bold text-cyan-600">{formatCurrency(selectedOrder.selling_price)}</p>
                </div>
              </div>
            </div>
            <div className="mt-6 flex gap-2">
              <Button className="bg-cyan-600 hover:bg-cyan-700">Edit Order</Button>
              <Button variant="ghost">View Invoice</Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};
