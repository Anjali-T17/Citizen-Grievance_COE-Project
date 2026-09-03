import React, { useState, useEffect } from 'react';
import { analyticsAPI } from '../services/api';
import { BarChart3, TrendingDown, HelpCircle, Activity, RefreshCw, Loader2 } from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend
} from 'recharts';

export const AnalyticsPage = () => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    setIsLoading(true);
    try {
      const res = await analyticsAPI.getUsageAnalytics();
      setData(res.data);
    } catch (err) {
      console.error('Failed to fetch usage analytics:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const COLORS = ['#38bdf8', '#818cf8', '#fbbf24', '#f87171', '#34d399'];

  if (isLoading) {
    return (
      <div className="p-12 text-center text-slate-400">
        <Loader2 className="w-8 h-8 animate-spin mx-auto text-sky-400 mb-2" />
        <p className="text-xs">Computing feature usage analytics from SQLite usage_events...</p>
      </div>
    );
  }

  const allFeaturesChartData = [
    ...(data?.most_used_features || []),
    ...(data?.underused_features || []),
  ];

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-2xl font-black text-white flex items-center gap-2.5">
            <BarChart3 className="w-6 h-6 text-sky-400" />
            <span>Feature Usage & Discovery Analytics</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time analytics computed dynamically from SQLite usage events and override logs
          </p>
        </div>

        <button
          onClick={fetchAnalytics}
          className="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 rounded-xl border border-slate-700 transition-colors flex items-center gap-1.5"
        >
          <RefreshCw className="w-3.5 h-3.5 text-sky-400" />
          <span>Refresh Data</span>
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-xs text-slate-400 font-semibold uppercase">
            <span>Total Usage Events</span>
            <Activity className="w-4 h-4 text-sky-400" />
          </div>
          <p className="text-3xl font-black text-white">{data?.total_usage_events || 0}</p>
          <p className="text-[11px] text-slate-500">Tracked actions in usage_events table</p>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-xs text-slate-400 font-semibold uppercase">
            <span>Assistant Recommendations</span>
            <BarChart3 className="w-4 h-4 text-indigo-400" />
          </div>
          <p className="text-3xl font-black text-indigo-300">{data?.total_recommendations || 0}</p>
          <p className="text-[11px] text-slate-500">Generated explainable recommendations</p>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-xs text-slate-400 font-semibold uppercase">
            <span>Override Logged Count</span>
            <HelpCircle className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-3xl font-black text-amber-300">{data?.total_overrides || 0}</p>
          <p className="text-[11px] text-slate-500">Captured human override reasons</p>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Feature Usage Bar Chart */}
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4 shadow-xl">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-sky-400" />
              <span>Feature Usage Frequency Distribution</span>
            </h3>
            <span className="text-[11px] text-slate-400">Events Count</span>
          </div>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={allFeaturesChartData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <XAxis dataKey="feature_id" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px' }}
                  labelStyle={{ color: '#38bdf8', fontWeight: 'bold' }}
                />
                <Bar dataKey="usage_count" radius={[6, 6, 0, 0]}>
                  {allFeaturesChartData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={entry.underused ? '#fbbf24' : '#38bdf8'}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="flex items-center justify-center gap-6 text-xs text-slate-400">
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded bg-sky-400"></span>
              <span>Standard Usage</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded bg-amber-400"></span>
              <span>Underused Feature (Target for Discovery)</span>
            </div>
          </div>
        </div>

        {/* Underused Features List & Override Reasons */}
        <div className="space-y-6">
          {/* Underused Features Alert Box */}
          <div className="glass-panel p-5 rounded-2xl border border-amber-500/30 space-y-3">
            <div className="flex items-center gap-2">
              <TrendingDown className="w-5 h-5 text-amber-400" />
              <h3 className="text-sm font-bold text-amber-300">Underused Features Requiring Discovery Boost</h3>
            </div>
            <div className="space-y-2">
              {data?.underused_features?.map((feat) => (
                <div key={feat.feature_id} className="p-3 bg-slate-900/60 rounded-xl border border-slate-800 flex items-center justify-between text-xs">
                  <div>
                    <span className="font-bold text-white">{feat.feature_name} ({feat.feature_id})</span>
                    <p className="text-[11px] text-slate-400">Boosted in recommendation algorithm (+10 pts)</p>
                  </div>
                  <span className="px-2.5 py-1 rounded bg-amber-500/10 text-amber-300 font-bold border border-amber-500/20">
                    {feat.usage_count} usage events
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Override Reasons Pie Chart */}
          <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-3">
            <h3 className="text-sm font-bold text-white">Override Reasons Distribution</h3>
            {data?.override_reasons?.length === 0 ? (
              <p className="text-xs text-slate-500 py-4 text-center">No human overrides recorded yet.</p>
            ) : (
              <div className="h-44">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={data?.override_reasons}
                      dataKey="count"
                      nameKey="reason"
                      cx="50%"
                      cy="50%"
                      outerRadius={60}
                      label
                    >
                      {data?.override_reasons?.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} />
                    <Legend wrapperStyle={{ fontSize: '11px', color: '#94a3b8' }} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
