import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  FilePlus,
  History,
  Search,
  Languages,
  FileCheck,
  AlertTriangle,
  FileText,
  BarChart3,
  Layers,
  LayoutDashboard,
  Upload
} from 'lucide-react';

export const Sidebar = () => {
  const { user } = useAuth();
  const role = user?.role || 'Citizen';

  const navItemsByRole = {
    'Citizen': [
      { path: '/', label: 'Overview', icon: LayoutDashboard },
      { path: '/submit-complaint', label: 'Submit Complaint', icon: FilePlus },
      { path: '/my-complaints', label: 'My Complaints', icon: History },
      { path: '/features', label: 'Feature Catalog', icon: Layers },
    ],
    'Grievance Officer': [
      { path: '/', label: 'Officer Dashboard', icon: LayoutDashboard },
      { path: '/my-complaints', label: 'Assigned Complaints', icon: History },
      { path: '/features', label: 'Feature Catalog', icon: Layers },
      { path: '/analytics', label: 'Usage Analytics', icon: BarChart3 },
    ],
    'Supervisor': [
      { path: '/', label: 'Supervisor Dashboard', icon: LayoutDashboard },
      { path: '/analytics', label: 'Usage Analytics', icon: BarChart3 },
      { path: '/my-complaints', label: 'Complaint Monitoring', icon: History },
      { path: '/features', label: 'Feature Catalog', icon: Layers },
    ],
    'External Partner': [
      { path: '/', label: 'Partner Dashboard', icon: LayoutDashboard },
      { path: '/my-complaints', label: 'Assigned Complaints', icon: History },
      { path: '/features', label: 'Feature Catalog', icon: Layers },
    ],
  };

  const navItems = navItemsByRole[role] || navItemsByRole['Citizen'];

  return (
    <aside className="w-64 bg-slate-900/90 border-r border-slate-800 flex flex-col justify-between min-h-[calc(100vh-4rem)] p-4">
      <div className="space-y-6">
        <div>
          <p className="px-3 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Navigation</p>
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-sky-500/10 text-sky-400 border border-sky-500/20'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                    }`
                  }
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </nav>
        </div>

        {/* Allowed Features Quick List */}
        <div className="border-t border-slate-800/80 pt-4">
          <p className="px-3 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Permitted Role Features</p>
          <div className="space-y-1.5 px-3">
            {role === 'Citizen' && (
              <>
                <span className="inline-block text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded border border-slate-700">F001 - Submit Complaint</span>
                <span className="inline-block text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded border border-slate-700">F002 - Track Complaint</span>
              </>
            )}
            {role === 'Grievance Officer' && (
              <>
                <span className="inline-block text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded border border-slate-700">F003 - Translate Complaint</span>
                <span className="inline-block text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded border border-slate-700">F004 - Verify Attachment</span>
                <span className="inline-block text-xs bg-amber-500/10 text-amber-300 px-2 py-1 rounded border border-amber-500/30">F005 - Escalate (High Impact)</span>
                <span className="inline-block text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded border border-slate-700">F006 - Internal Notes</span>
              </>
            )}
            {role === 'Supervisor' && (
              <>
                <span className="inline-block text-xs bg-purple-500/10 text-purple-300 px-2 py-1 rounded border border-purple-500/30">F007 - Complaint Monitoring</span>
                <span className="inline-block text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded border border-slate-700">F003 - Translate Complaint</span>
                <span className="inline-block text-xs bg-amber-500/10 text-amber-300 px-2 py-1 rounded border border-amber-500/30">F005 - Escalate Complaint</span>
              </>
            )}
            {role === 'External Partner' && (
              <>
                <span className="inline-block text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded border border-slate-700">F008 - Upload Evidence</span>
                <span className="inline-block text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded border border-slate-700">F004 - Verify Attachment</span>
              </>
            )}
          </div>
        </div>
      </div>

      <div className="p-3 bg-slate-800/40 rounded-xl border border-slate-800 text-xs text-slate-400">
        <p className="font-semibold text-slate-300 mb-1">Phase 1 Evaluation Status</p>
        <div className="w-full bg-slate-700 h-2 rounded-full overflow-hidden mb-1.5">
          <div className="bg-sky-400 h-full w-[35%]"></div>
        </div>
        <p className="text-[11px] text-sky-400">Phase 1 Scope Complete (35%)</p>
      </div>
    </aside>
  );
};
