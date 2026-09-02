import { format, parseISO, formatDistanceToNow } from 'date-fns';

export const formatDate = (date: string | Date): string => {
  const d = typeof date === 'string' ? parseISO(date) : date;
  return format(d, 'MMM dd, yyyy');
};

export const formatDateTime = (date: string | Date): string => {
  const d = typeof date === 'string' ? parseISO(date) : date;
  return format(d, 'MMM dd, yyyy HH:mm');
};

export const formatTimeAgo = (date: string | Date): string => {
  const d = typeof date === 'string' ? parseISO(date) : date;
  return formatDistanceToNow(d, { addSuffix: true });
};

export const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(value);
};

export const formatNumber = (value: number, decimals = 2): string => {
  return Number(value).toFixed(decimals);
};

export const formatPercentage = (value: number, decimals = 1): string => {
  return `${Number(value).toFixed(decimals)}%`;
};

export const formatQuantity = (value: number, unit: string): string => {
  return `${Number(value).toFixed(2)} ${unit}`;
};

export const calculateProfit = (revenue: number, cost: number): number => {
  return revenue - cost;
};

export const calculateProfitMargin = (revenue: number, cost: number): number => {
  if (revenue === 0) return 0;
  return ((revenue - cost) / revenue) * 100;
};

export const formatOrderStatus = (status: string): string => {
  const statusMap: Record<string, string> = {
    QUOTE: 'Quote',
    CONFIRMED: 'Confirmed',
    IN_PROGRESS: 'In Progress',
    COMPLETED: 'Completed',
    CANCELLED: 'Cancelled',
  };
  return statusMap[status] || status;
};

export const getStatusColor = (status: string): string => {
  const colorMap: Record<string, string> = {
    QUOTE: 'bg-gray-100 text-gray-800',
    CONFIRMED: 'bg-blue-100 text-blue-800',
    IN_PROGRESS: 'bg-yellow-100 text-yellow-800',
    COMPLETED: 'bg-green-100 text-green-800',
    CANCELLED: 'bg-red-100 text-red-800',
  };
  return colorMap[status] || 'bg-gray-100 text-gray-800';
};

export const getStatusBgColor = (status: string): string => {
  const bgColorMap: Record<string, string> = {
    QUOTE: 'bg-gray-50',
    CONFIRMED: 'bg-blue-50',
    IN_PROGRESS: 'bg-yellow-50',
    COMPLETED: 'bg-green-50',
    CANCELLED: 'bg-red-50',
  };
  return bgColorMap[status] || 'bg-gray-50';
};
