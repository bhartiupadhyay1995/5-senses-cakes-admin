import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown, DollarSign, Percent, PieChart as PieChartIcon } from 'lucide-react';
import { formatCurrency } from '../utils/formatters';

const monthlyData = [
  { month: 'Jan', revenue: 4200, costs: 2400, profit: 1800 },
  { month: 'Feb', revenue: 3800, costs: 2210, profit: 1590 },
  { month: 'Mar', revenue: 5200, costs: 2290, profit: 2910 },
  { month: 'Apr', revenue: 4890, costs: 2000, profit: 2890 },
  { month: 'May', revenue: 6200, costs: 2181, profit: 4019 },
  { month: 'Jun', revenue: 5800, costs: 2500, profit: 3300 },
];

const profitMarginData = [
  { name: 'Chocolate', value: 42 },
  { name: 'Vanilla', value: 38 },
  { name: 'Red Velvet', value: 45 },
  { name: 'Custom', value: 35 },
];

const metricCards = [
  {
    title: 'Total Revenue',
    value: '$29,890',
    change: '+12.5%',
    trend: 'up',
    icon: <DollarSign className="h-8 w-8 text-emerald-600" />,
    tone: 'bg-emerald-50 border-emerald-100',
  },
  {
    title: 'Total Costs',
    value: '$14,581',
    change: '+5.2%',
    trend: 'up',
    icon: <DollarSign className="h-8 w-8 text-amber-600" />,
    tone: 'bg-amber-50 border-amber-100',
  },
  {
    title: 'Gross Profit',
    value: '$15,309',
    change: '+18.3%',
    trend: 'up',
    icon: <TrendingUp className="h-8 w-8 text-green-600" />,
    tone: 'bg-green-50 border-green-100',
  },
  {
    title: 'Margin %',
    value: '51.2%',
    change: '+2.1%',
    trend: 'up',
    icon: <Percent className="h-8 w-8 text-violet-600" />,
    tone: 'bg-violet-50 border-violet-100',
  },
];

export const ProfitabilityPage: React.FC = () => {
  const [timeRange, setTimeRange] = useState('6m');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="rounded-3xl bg-gradient-to-r from-green-500 via-emerald-500 to-teal-400 p-6 text-white shadow-lg shadow-green-200/60">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <div className="mb-2 inline-flex items-center gap-2 rounded-full bg-white/15 px-3 py-1 text-xs font-semibold tracking-wide uppercase text-green-50">
              <PieChartIcon className="h-3.5 w-3.5" />
              Financial analysis
            </div>
            <h1 className="text-3xl font-bold tracking-tight">Profitability</h1>
            <p className="mt-2 max-w-xl text-sm text-green-50/90">Monitor revenue, costs, and profit margins across all orders and recipes.</p>
          </div>
        </div>
      </div>

      {/* Time Range Filter */}
      <Card className="border-green-100">
        <CardContent className="pt-6">
          <div className="flex flex-wrap gap-2">
            {['1m', '3m', '6m', '1y'].map((range) => (
              <Button
                key={range}
                variant={timeRange === range ? 'default' : 'ghost'}
                onClick={() => setTimeRange(range)}
                className={timeRange === range ? 'bg-gradient-to-r from-green-500 to-emerald-500 text-white' : ''}
              >
                {range === '1m' ? 'Last Month' : range === '3m' ? 'Last 3 Months' : range === '6m' ? 'Last 6 Months' : 'Last Year'}
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Key Metrics */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {metricCards.map((card) => (
          <Card key={card.title} className={`${card.tone} border`}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-700">{card.title}</CardTitle>
              <div className="rounded-lg bg-white/80 p-2 shadow-sm">{card.icon}</div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-slate-900">{card.value}</div>
              <div className="mt-1 flex items-center gap-1">
                {card.trend === 'up' ? (
                  <TrendingUp className="h-4 w-4 text-green-600" />
                ) : (
                  <TrendingDown className="h-4 w-4 text-red-600" />
                )}
                <p className={`text-xs font-medium ${card.trend === 'up' ? 'text-green-700' : 'text-red-700'}`}>{card.change}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Revenue vs Costs Chart */}
      <Card className="border-green-100 bg-gradient-to-br from-white to-green-50/30">
        <CardHeader>
          <CardTitle>Revenue & Costs</CardTitle>
          <CardDescription>Monthly revenue, costs, and profit trend</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip formatter={(value) => formatCurrency(value as number)} />
              <Legend />
              <Line type="monotone" dataKey="revenue" stroke="#10b981" strokeWidth={2} name="Revenue" />
              <Line type="monotone" dataKey="costs" stroke="#f59e0b" strokeWidth={2} name="Costs" />
              <Line type="monotone" dataKey="profit" stroke="#8b5cf6" strokeWidth={2} name="Profit" />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Profit by Month Chart */}
      <Card className="border-green-100 bg-gradient-to-br from-white to-emerald-50/30">
        <CardHeader>
          <CardTitle>Monthly Profit</CardTitle>
          <CardDescription>Profit breakdown by month</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip formatter={(value) => formatCurrency(value as number)} />
              <Legend />
              <Bar dataKey="profit" fill="#10b981" name="Profit" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Profit Margin by Recipe */}
      <div className="grid gap-4 lg:grid-cols-2">
        <Card className="border-green-100 bg-gradient-to-br from-white to-teal-50/30">
          <CardHeader>
            <CardTitle>Profit Margin by Recipe</CardTitle>
            <CardDescription>Average margin percentage</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {profitMarginData.map((item) => (
                <div key={item.name}>
                  <div className="flex justify-between text-sm">
                    <span className="font-medium text-slate-900">{item.name}</span>
                    <span className="font-semibold text-emerald-600">{item.value}%</span>
                  </div>
                  <div className="mt-1 h-2 rounded-full bg-slate-100">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-teal-500"
                      style={{ width: `${item.value}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card className="border-green-100 bg-gradient-to-br from-white to-green-50/30">
          <CardHeader>
            <CardTitle>Quick Stats</CardTitle>
            <CardDescription>Key performance indicators</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-4">
                <p className="text-sm text-emerald-700">Avg Order Value</p>
                <p className="text-2xl font-bold text-emerald-900">$435.50</p>
              </div>
              <div className="rounded-lg border border-teal-200 bg-teal-50 p-4">
                <p className="text-sm text-teal-700">Cost per Item</p>
                <p className="text-2xl font-bold text-teal-900">$28.45</p>
              </div>
              <div className="rounded-lg border border-green-200 bg-green-50 p-4">
                <p className="text-sm text-green-700">Profit per Item</p>
                <p className="text-2xl font-bold text-green-900">$42.80</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
