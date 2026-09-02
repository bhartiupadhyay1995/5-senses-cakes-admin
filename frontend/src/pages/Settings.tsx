import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Settings as SettingsIcon, User, Lock, Bell, Palette, Database, LogOut } from 'lucide-react';

interface SettingSection {
  id: string;
  title: string;
  description: string;
  icon: React.ReactNode;
}

const settingSections: SettingSection[] = [
  {
    id: 'business',
    title: 'Business Settings',
    description: 'Configure your business details and preferences',
    icon: <SettingsIcon className="h-5 w-5" />,
  },
  {
    id: 'profile',
    title: 'Profile',
    description: 'Manage your personal account settings',
    icon: <User className="h-5 w-5" />,
  },
  {
    id: 'security',
    title: 'Security',
    description: 'Manage passwords and authentication settings',
    icon: <Lock className="h-5 w-5" />,
  },
  {
    id: 'notifications',
    title: 'Notifications',
    description: 'Control how you receive alerts and updates',
    icon: <Bell className="h-5 w-5" />,
  },
  {
    id: 'appearance',
    title: 'Appearance',
    description: 'Customize theme and visual preferences',
    icon: <Palette className="h-5 w-5" />,
  },
  {
    id: 'data',
    title: 'Data & Export',
    description: 'Backup and export your business data',
    icon: <Database className="h-5 w-5" />,
  },
];

export const SettingsPage: React.FC = () => {
  const [selectedSection, setSelectedSection] = useState('business');

  const renderContent = () => {
    switch (selectedSection) {
      case 'business':
        return (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700">Business Name</label>
              <input
                type="text"
                defaultValue="5 Senses Cakes"
                className="mt-2 w-full rounded-lg border border-slate-200 px-3 py-2 text-sm focus:border-rose-500 focus:outline-none focus:ring-1 focus:ring-rose-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700">Email Address</label>
              <input
                type="email"
                defaultValue="contact@5sensescakes.com"
                className="mt-2 w-full rounded-lg border border-slate-200 px-3 py-2 text-sm focus:border-rose-500 focus:outline-none focus:ring-1 focus:ring-rose-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700">Phone Number</label>
              <input
                type="tel"
                defaultValue="+1 (555) 123-4567"
                className="mt-2 w-full rounded-lg border border-slate-200 px-3 py-2 text-sm focus:border-rose-500 focus:outline-none focus:ring-1 focus:ring-rose-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700">Address</label>
              <input
                type="text"
                defaultValue="123 Cake Street, Bakery City, CA 90210"
                className="mt-2 w-full rounded-lg border border-slate-200 px-3 py-2 text-sm focus:border-rose-500 focus:outline-none focus:ring-1 focus:ring-rose-500"
              />
            </div>
          </div>
        );
      case 'profile':
        return (
          <div className="space-y-4">
            <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
              <div className="flex items-center gap-4">
                <div className="h-12 w-12 rounded-full bg-gradient-to-br from-rose-500 to-pink-500" />
                <div>
                  <p className="font-semibold text-slate-900">Jane Baker</p>
                  <p className="text-sm text-slate-600">Owner</p>
                </div>
                <Button variant="ghost" className="ml-auto">Upload Photo</Button>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700">Full Name</label>
              <input
                type="text"
                defaultValue="Jane Baker"
                className="mt-2 w-full rounded-lg border border-slate-200 px-3 py-2 text-sm focus:border-rose-500 focus:outline-none focus:ring-1 focus:ring-rose-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700">Email Address</label>
              <input
                type="email"
                defaultValue="jane@5sensescakes.com"
                className="mt-2 w-full rounded-lg border border-slate-200 px-3 py-2 text-sm focus:border-rose-500 focus:outline-none focus:ring-1 focus:ring-rose-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700">Role</label>
              <select className="mt-2 w-full rounded-lg border border-slate-200 px-3 py-2 text-sm focus:border-rose-500 focus:outline-none focus:ring-1 focus:ring-rose-500">
                <option>Owner</option>
                <option>Manager</option>
                <option>Staff</option>
              </select>
            </div>
          </div>
        );
      case 'security':
        return (
          <div className="space-y-4">
            <div className="rounded-lg border border-amber-200 bg-amber-50 p-4">
              <p className="text-sm font-medium text-amber-900">Password Last Changed</p>
              <p className="mt-1 text-sm text-amber-800">45 days ago</p>
            </div>
            <Button variant="ghost" className="w-full justify-start border border-slate-200">
              Change Password
            </Button>
            <div className="pt-4">
              <h3 className="font-semibold text-slate-900">Two-Factor Authentication</h3>
              <p className="mt-1 text-sm text-slate-600">Add extra security to your account</p>
              <Button className="mt-3 bg-rose-600 hover:bg-rose-700">Enable 2FA</Button>
            </div>
            <div className="space-y-2 border-t border-slate-200 pt-4">
              <h3 className="font-semibold text-slate-900">Active Sessions</h3>
              <div className="space-y-2">
                <div className="flex items-center justify-between rounded-lg border border-slate-200 p-3">
                  <div>
                    <p className="text-sm font-medium text-slate-900">Chrome on macOS</p>
                    <p className="text-xs text-slate-600">Last active 5 minutes ago</p>
                  </div>
                  <span className="text-xs font-semibold text-emerald-600">Active</span>
                </div>
              </div>
            </div>
          </div>
        );
      case 'notifications':
        return (
          <div className="space-y-4">
            <div className="space-y-3">
              <div className="flex items-center justify-between rounded-lg border border-slate-200 p-4">
                <div>
                  <p className="font-medium text-slate-900">Order Reminders</p>
                  <p className="text-sm text-slate-600">Get notified about upcoming orders</p>
                </div>
                <input type="checkbox" defaultChecked className="h-4 w-4 rounded" />
              </div>
              <div className="flex items-center justify-between rounded-lg border border-slate-200 p-4">
                <div>
                  <p className="font-medium text-slate-900">Low Stock Alerts</p>
                  <p className="text-sm text-slate-600">Alerts when ingredients run low</p>
                </div>
                <input type="checkbox" defaultChecked className="h-4 w-4 rounded" />
              </div>
              <div className="flex items-center justify-between rounded-lg border border-slate-200 p-4">
                <div>
                  <p className="font-medium text-slate-900">Daily Summary</p>
                  <p className="text-sm text-slate-600">Daily summary of business activities</p>
                </div>
                <input type="checkbox" className="h-4 w-4 rounded" />
              </div>
              <div className="flex items-center justify-between rounded-lg border border-slate-200 p-4">
                <div>
                  <p className="font-medium text-slate-900">Weekly Reports</p>
                  <p className="text-sm text-slate-600">Weekly profitability and order reports</p>
                </div>
                <input type="checkbox" defaultChecked className="h-4 w-4 rounded" />
              </div>
            </div>
          </div>
        );
      case 'appearance':
        return (
          <div className="space-y-4">
            <div>
              <p className="font-medium text-slate-900">Theme</p>
              <div className="mt-2 space-y-2">
                <label className="flex items-center gap-3 rounded-lg border border-slate-200 p-3">
                  <input type="radio" name="theme" defaultChecked className="h-4 w-4" />
                  <span className="text-sm font-medium text-slate-900">Light</span>
                </label>
                <label className="flex items-center gap-3 rounded-lg border border-slate-200 p-3">
                  <input type="radio" name="theme" className="h-4 w-4" />
                  <span className="text-sm font-medium text-slate-900">Dark</span>
                </label>
                <label className="flex items-center gap-3 rounded-lg border border-slate-200 p-3">
                  <input type="radio" name="theme" className="h-4 w-4" />
                  <span className="text-sm font-medium text-slate-900">Auto</span>
                </label>
              </div>
            </div>
            <div className="pt-4">
              <p className="font-medium text-slate-900">Brand Color</p>
              <div className="mt-2 flex gap-3">
                <button className="h-10 w-10 rounded-lg bg-rose-500 ring-2 ring-rose-300" />
                <button className="h-10 w-10 rounded-lg bg-pink-500 ring-2 ring-pink-100" />
                <button className="h-10 w-10 rounded-lg bg-purple-500 ring-2 ring-purple-100" />
              </div>
            </div>
          </div>
        );
      case 'data':
        return (
          <div className="space-y-4">
            <div className="rounded-lg border border-cyan-200 bg-cyan-50 p-4">
              <p className="text-sm font-medium text-cyan-900">Last Backup</p>
              <p className="mt-1 text-sm text-cyan-800">January 19, 2024 at 3:15 PM</p>
            </div>
            <Button variant="ghost" className="w-full justify-start border border-slate-200">
              Backup Now
            </Button>
            <Button variant="ghost" className="w-full justify-start border border-slate-200">
              View Backups
            </Button>
            <div className="space-y-2 border-t border-slate-200 pt-4">
              <h3 className="font-semibold text-slate-900">Export Data</h3>
              <p className="text-sm text-slate-600">Download your data in CSV or JSON format</p>
              <div className="flex gap-2 pt-2">
                <Button variant="ghost" className="flex-1 border border-slate-200">
                  Export CSV
                </Button>
                <Button variant="ghost" className="flex-1 border border-slate-200">
                  Export JSON
                </Button>
              </div>
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="rounded-3xl bg-gradient-to-r from-slate-700 via-slate-600 to-slate-500 p-6 text-white shadow-lg shadow-slate-400/60">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <div className="mb-2 inline-flex items-center gap-2 rounded-full bg-white/15 px-3 py-1 text-xs font-semibold tracking-wide uppercase text-slate-100">
              <SettingsIcon className="h-3.5 w-3.5" />
              Configuration
            </div>
            <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
            <p className="mt-2 max-w-xl text-sm text-slate-200/90">Manage your account, business, and application preferences.</p>
          </div>
        </div>
      </div>

      {/* Settings Navigation */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {settingSections.map((section) => (
          <Card
            key={section.id}
            className={`cursor-pointer border transition-all ${
              selectedSection === section.id
                ? 'border-slate-500 bg-slate-50 ring-2 ring-slate-500/20'
                : 'border-slate-200 hover:border-slate-300 hover:shadow-md'
            }`}
            onClick={() => setSelectedSection(section.id)}
          >
            <CardContent className="pt-6">
              <div className="flex items-start gap-3">
                <div className="rounded-lg bg-slate-100 p-2 text-slate-700">{section.icon}</div>
                <div>
                  <h3 className="font-semibold text-slate-900">{section.title}</h3>
                  <p className="mt-1 text-xs text-slate-600">{section.description}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Settings Content */}
      <Card className="border-slate-200">
        <CardHeader>
          <CardTitle>{settingSections.find((s) => s.id === selectedSection)?.title}</CardTitle>
          <CardDescription>{settingSections.find((s) => s.id === selectedSection)?.description}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="max-w-2xl">{renderContent()}</div>
          <div className="mt-6 flex gap-3 border-t border-slate-200 pt-6">
            <Button className="bg-slate-700 hover:bg-slate-800">Save Changes</Button>
            <Button variant="ghost">Cancel</Button>
          </div>
        </CardContent>
      </Card>

      {/* Logout */}
      <Card className="border-red-200 bg-red-50/50">
        <CardContent className="pt-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-semibold text-red-900">Sign Out</h3>
              <p className="mt-1 text-sm text-red-800">Sign out from your account on this device</p>
            </div>
            <Button variant="ghost" className="border border-red-200 text-red-600 hover:bg-red-100 hover:text-red-700">
              <LogOut className="mr-2 h-4 w-4" />
              Sign Out
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
