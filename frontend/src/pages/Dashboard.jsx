import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { complaintAPI } from '../services/api';
import { AssistantPanel } from '../components/AssistantPanel';
import { LayoutDashboard, FileText, Globe, Shield, ArrowRight, CheckCircle2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const role = user?.role || 'Citizen';

  const [complaints, setComplaints] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchRecentComplaints();
  }, []);

  const fetchRecentComplaints = async () => {
    setIsLoading(true);
    try {
      const res = await complaintAPI.getComplaints();
      setComplaints(res.data.slice(0, 5));
    } catch (err) {
      console.error('Failed to load recent complaints:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="p-6 rounded-3xl bg-gradient-to-r from-slate-900 via-slate-800 to-indigo-950 border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-2xl">
        <div className="space-y-1">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20 text-xs font-semibold">
            <span>Logged in as {user?.role}</span>
          </div>
          <h1 className="text-2xl font-black text-white">
            Welcome, {user?.name || 'Citizen'}!
          </h1>
          <p className="text-xs text-slate-300">
            {user?.organisation} • Role-Aware Feature Discovery Engine (Phase 1 Review 1 MVP)
          </p>
        </div>

        <div className="flex items-center gap-3">
          {role === 'Citizen' && (
            <button
              onClick={() => navigate('/submit-complaint')}
              className="px-4 py-2.5 bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold rounded-xl text-xs transition-colors shadow-lg shadow-sky-500/20"
            >
              + Submit Complaint
            </button>
          )}
          <button
            onClick={() => navigate('/features')}
            className="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold rounded-xl text-xs border border-slate-700 transition-colors"
          >
            Explore Feature Catalog
          </button>
        </div>
      </div>

      {/* Main Grid: Dashboard Widgets + Embedded Assistant */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Stats & Complaints (7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          {/* Quick Metrics */}
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            <div className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 space-y-1">
              <span className="text-[11px] font-semibold text-slate-500 uppercase">Active Complaints</span>
              <p className="text-2xl font-black text-white">{complaints.length}</p>
            </div>
            <div className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 space-y-1">
              <span className="text-[11px] font-semibold text-slate-500 uppercase">Multilingual Input</span>
              <p className="text-2xl font-black text-sky-400">Tamil & Hindi</p>
            </div>
            <div className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 space-y-1 col-span-2 sm:col-span-1">
              <span className="text-[11px] font-semibold text-slate-500 uppercase">System Status</span>
              <p className="text-xs font-extrabold text-emerald-400 flex items-center gap-1 mt-1">
                <CheckCircle2 className="w-3.5 h-3.5" /> SQLite Active
              </p>
            </div>
          </div>

          {/* Recent Complaints Table Preview */}
          <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-3 shadow-xl">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <FileText className="w-4 h-4 text-sky-400" />
                <span>Recent Grievance Complaints</span>
              </h3>
              <button
                onClick={() => navigate('/my-complaints')}
                className="text-xs text-sky-400 hover:text-sky-300 font-semibold flex items-center gap-1"
              >
                <span>View All</span>
                <ArrowRight className="w-3 h-3" />
              </button>
            </div>

            <div className="space-y-2">
              {complaints.map((item) => (
                <div
                  key={item.complaint_id}
                  onClick={() => navigate(`/complaints/${item.complaint_id}`)}
                  className="p-3 bg-slate-900/60 hover:bg-slate-800/80 rounded-xl border border-slate-800 transition-colors cursor-pointer flex items-center justify-between text-xs"
                >
                  <div className="space-y-0.5">
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-bold text-sky-400">{item.complaint_id}</span>
                      <span className="text-slate-300 font-medium">{item.category}</span>
                    </div>
                    <p className="text-slate-400 line-clamp-1 max-w-sm">{item.description}</p>
                  </div>

                  <div className="text-right space-y-1 shrink-0 ml-2">
                    <span
                      className={`inline-block px-2 py-0.5 rounded text-[10px] font-bold border ${
                        item.language === 'Tamil'
                          ? 'bg-sky-500/10 text-sky-300 border-sky-500/30'
                          : 'bg-purple-500/10 text-purple-300 border-purple-500/30'
                      }`}
                    >
                      {item.language}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Embedded Role-Aware Feature Discovery Assistant (5 cols) */}
        <div className="lg:col-span-5">
          <AssistantPanel />
        </div>
      </div>
    </div>
  );
};
