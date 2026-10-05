import React, { useState, useEffect } from 'react';
import { analyticsAPI, experimentAPI, stakeholderAPI } from '../services/api';
import {
  BarChart3,
  TrendingDown,
  HelpCircle,
  Activity,
  RefreshCw,
  Loader2,
  Award,
  ShieldAlert,
  Users,
  CheckCircle2,
  PlusCircle,
  X,
  Star,
  Sparkles
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';

export const AnalyticsPage = () => {
  const [data, setData] = useState(null);
  const [experiments, setExperiments] = useState(null);
  const [upliftData, setUpliftData] = useState(null);
  const [errors, setErrors] = useState([]);
  const [stakeholders, setStakeholders] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Stakeholder Modal Form state
  const [isValidationModalOpen, setIsValidationModalOpen] = useState(false);
  const [submittingValidation, setSubmittingValidation] = useState(false);
  const [validationSuccess, setValidationSuccess] = useState('');
  const [validationError, setValidationError] = useState('');

  const [stakeholderRole, setStakeholderRole] = useState('Routing Officer');
  const [usabilityRating, setUsabilityRating] = useState(5);
  const [explainabilityRating, setExplainabilityRating] = useState(5);
  const [speedupPct, setSpeedupPct] = useState(45);
  const [feedbackNotes, setFeedbackNotes] = useState('');

  useEffect(() => {
    fetchAllAnalytics();
  }, []);

  const fetchAllAnalytics = async () => {
    setIsLoading(true);
    try {
      const [uRes, eRes, errRes, sRes, upRes] = await Promise.all([
        analyticsAPI.getUsageAnalytics(),
        experimentAPI.getExperimentMetrics(),
        analyticsAPI.getErrorAnalysis(),
        stakeholderAPI.getSummary(),
        analyticsAPI.getDiscoveryUplift(),
      ]);
      setData(uRes.data);
      setExperiments(eRes.data);
      setErrors(errRes.data);
      setStakeholders(sRes.data);
      setUpliftData(upRes.data);
    } catch (err) {
      console.error('Failed to fetch analytics:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleValidationSubmit = async (e) => {
    e.preventDefault();
    setSubmittingValidation(true);
    setValidationSuccess('');
    setValidationError('');

    try {
      await stakeholderAPI.submitValidation({
        stakeholder_role: stakeholderRole,
        usability_rating: Number(usabilityRating),
        explainability_rating: Number(explainabilityRating),
        routing_speedup_pct: Number(speedupPct),
        feedback_notes: feedbackNotes,
      });

      setValidationSuccess('Stakeholder validation recorded successfully!');
      setFeedbackNotes('');
      // Refresh stakeholder summary and uplift data
      const [sRes, upRes] = await Promise.all([
        stakeholderAPI.getSummary(),
        analyticsAPI.getDiscoveryUplift(),
      ]);
      setStakeholders(sRes.data);
      setUpliftData(upRes.data);

      setTimeout(() => {
        setIsValidationModalOpen(false);
        setValidationSuccess('');
      }, 1500);
    } catch (err) {
      console.error('Failed to submit stakeholder validation:', err);
      setValidationError(
        err.response?.data?.detail || 'Failed to submit validation to backend server.'
      );
    } finally {
      setSubmittingValidation(false);
    }
  };

  if (isLoading) {
    return (
      <div className="p-12 text-center text-slate-400">
        <Loader2 className="w-8 h-8 animate-spin mx-auto text-sky-400 mb-2" />
        <p className="text-xs">Computing feature usage, A/B experiments, uplift analytics, and error analysis...</p>
      </div>
    );
  }

  const featureLevelList = upliftData?.feature_level_results
    ? Object.values(upliftData.feature_level_results)
    : [];

  const abChartData = [
    {
      metric: 'Discovery Rate (%)',
      Baseline: upliftData?.baseline_discovery_rate ?? 0,
      Assistant: upliftData?.assistant_discovery_rate ?? 0,
    },
    {
      metric: 'Completion Rate (%)',
      Baseline: upliftData?.baseline_completion_rate ?? 0,
      Assistant: upliftData?.assistant_completion_rate ?? 0,
    },
  ];

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-2xl font-black text-white flex items-center gap-2.5">
            <BarChart3 className="w-6 h-6 text-sky-400" />
            <span>Full System Analytics & Discovery Uplift Evaluation</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time discovery metrics, A/B baseline experiment results, and stakeholder evaluation
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsValidationModalOpen(true)}
            className="px-3.5 py-2 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-400 hover:to-purple-500 text-xs font-bold text-white rounded-xl shadow-md transition-all flex items-center gap-1.5"
          >
            <PlusCircle className="w-4 h-4" />
            <span>Validate System</span>
          </button>
          <button
            onClick={fetchAllAnalytics}
            className="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 rounded-xl border border-slate-700 transition-colors flex items-center gap-1.5"
          >
            <RefreshCw className="w-3.5 h-3.5 text-sky-400" />
            <span>Refresh Data</span>
          </button>
        </div>
      </div>

      {/* KPI Cards (C3 Discovery Uplift Metrics) */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-panel p-4 rounded-2xl border border-slate-800 space-y-1">
          <span className="text-[11px] font-semibold text-slate-500 uppercase">Discovery Uplift</span>
          <p className="text-3xl font-black text-emerald-400">
            {upliftData?.discovery_uplift_percentage > 0 ? '+' : ''}
            {upliftData?.discovery_uplift_percentage ?? 0}%
          </p>
          <p className="text-[11px] text-slate-400">
            Baseline: {upliftData?.baseline_discovery_rate}% → Assistant: {upliftData?.assistant_discovery_rate}%
          </p>
        </div>

        <div className="glass-panel p-4 rounded-2xl border border-slate-800 space-y-1">
          <span className="text-[11px] font-semibold text-slate-500 uppercase">Completion Uplift</span>
          <p className="text-3xl font-black text-sky-400">
            {upliftData?.completion_uplift_percentage > 0 ? '+' : ''}
            {upliftData?.completion_uplift_percentage ?? 0}%
          </p>
          <p className="text-[11px] text-slate-400">
            Baseline: {upliftData?.baseline_completion_rate}% → Assistant: {upliftData?.assistant_completion_rate}%
          </p>
        </div>

        <div className="glass-panel p-4 rounded-2xl border border-slate-800 space-y-1">
          <span className="text-[11px] font-semibold text-slate-500 uppercase">Total Usage Samples</span>
          <p className="text-3xl font-black text-indigo-400">
            {upliftData?.total_events ?? 0}
          </p>
          <p className="text-[11px] text-slate-400">Recorded across {upliftData?.total_users ?? 0} unique users</p>
        </div>

        <div className="glass-panel p-4 rounded-2xl border border-slate-800 space-y-1">
          <span className="text-[11px] font-semibold text-slate-500 uppercase">Usability Rating</span>
          <p className="text-3xl font-black text-amber-400">
            {stakeholders?.avg_usability_rating ?? 'N/A'}{' '}
            <span className="text-sm font-normal text-slate-400">/ 5</span>
          </p>
          <p className="text-[11px] text-slate-400">From {stakeholders?.total_validations ?? 0} stakeholder evaluations</p>
        </div>
      </div>

      {/* A/B Discovery & Completion Chart */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4 shadow-xl">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Award className="w-4 h-4 text-emerald-400" />
              <span>A/B Experiment Evaluation: Baseline vs Embedded Assistant</span>
            </h3>
            <p className="text-xs text-slate-400">
              Live database metrics: Discovery & Task Completion rates
            </p>
          </div>
          <span className="text-xs font-semibold px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            API Live Feed
          </span>
        </div>

        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={abChartData} margin={{ top: 10, right: 30, left: 0, bottom: 10 }}>
              <XAxis dataKey="metric" stroke="#94a3b8" fontSize={12} />
              <YAxis stroke="#94a3b8" fontSize={12} domain={[0, 100]} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px' }} />
              <Legend wrapperStyle={{ fontSize: '12px', color: '#cbd5e1' }} />
              <Bar dataKey="Baseline" fill="#475569" radius={[6, 6, 0, 0]} />
              <Bar dataKey="Assistant" fill="#10b981" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* C3 Feature-Level Uplift Table (F003, F006, F008) */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4 shadow-xl">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-sky-400" />
              <span>Feature-Level Discovery & Completion Uplift Breakdown</span>
            </h3>
            <p className="text-xs text-slate-400">
              Direct API response metrics for key grievance platform features (F003, F006, F008)
            </p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-900/80 text-slate-400 uppercase font-semibold text-[11px] border-b border-slate-800">
              <tr>
                <th className="py-3 px-4">Feature ID & Name</th>
                <th className="py-3 px-4 text-center">Baseline Disc.</th>
                <th className="py-3 px-4 text-center">Assistant Disc.</th>
                <th className="py-3 px-4 text-center">Disc. Uplift %</th>
                <th className="py-3 px-4 text-center">Baseline Comp.</th>
                <th className="py-3 px-4 text-center">Assistant Comp.</th>
                <th className="py-3 px-4 text-center">Comp. Uplift %</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {featureLevelList.length > 0 ? (
                featureLevelList.map((item) => (
                  <tr key={item.feature_id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3 px-4 font-medium text-white flex items-center gap-2">
                      <span className="font-mono text-xs text-sky-400 font-bold bg-sky-500/10 px-2 py-0.5 rounded border border-sky-500/20">
                        {item.feature_id}
                      </span>
                      <span>{item.feature_name}</span>
                    </td>
                    <td className="py-3 px-4 text-center font-mono text-slate-400">{item.baseline_discovery_rate}%</td>
                    <td className="py-3 px-4 text-center font-mono text-emerald-400 font-bold">{item.assistant_discovery_rate}%</td>
                    <td className="py-3 px-4 text-center">
                      <span className="px-2 py-0.5 rounded font-mono font-bold text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        +{item.discovery_uplift_percentage}%
                      </span>
                    </td>
                    <td className="py-3 px-4 text-center font-mono text-slate-400">{item.baseline_completion_rate}%</td>
                    <td className="py-3 px-4 text-center font-mono text-sky-400 font-bold">{item.assistant_completion_rate}%</td>
                    <td className="py-3 px-4 text-center">
                      <span className="px-2 py-0.5 rounded font-mono font-bold text-xs bg-sky-500/10 text-sky-400 border border-sky-500/20">
                        +{item.completion_uplift_percentage}%
                      </span>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="7" className="py-4 text-center text-slate-500">
                    No feature-level results found in database response.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Error Analysis & Stakeholder Summary Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Error Taxonomy Analysis */}
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4 shadow-xl">
          <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
            <ShieldAlert className="w-5 h-5 text-red-400" />
            <h3 className="text-sm font-bold text-white">System Error & Failure Mode Taxonomy</h3>
          </div>

          <div className="space-y-3">
            {errors.map((err, i) => (
              <div key={i} className="p-3.5 bg-slate-900/60 rounded-xl border border-slate-800 text-xs space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-white">{err.error_category}</span>
                  <span className="font-mono font-semibold text-sky-400 bg-sky-500/10 px-2 py-0.5 rounded border border-sky-500/20">
                    {err.percentage}% ({err.frequency} instances)
                  </span>
                </div>
                <p className="text-slate-400 text-[11px]">{err.root_cause_explanation}</p>
              </div>
            ))}
          </div>
        </div>

        {/* C5 Stakeholder Validation Summary */}
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4 shadow-xl">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="flex items-center gap-2">
              <Users className="w-5 h-5 text-indigo-400" />
              <h3 className="text-sm font-bold text-white">Stakeholder Validation Summary</h3>
            </div>

            <button
              onClick={() => setIsValidationModalOpen(true)}
              className="text-xs px-2.5 py-1 bg-indigo-500/20 hover:bg-indigo-500/30 text-indigo-300 rounded-lg border border-indigo-500/30 transition-colors flex items-center gap-1"
            >
              <PlusCircle className="w-3.5 h-3.5" />
              <span>Add Validation</span>
            </button>
          </div>

          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3 text-center">
              <div className="p-3 bg-slate-900 rounded-xl border border-slate-800">
                <p className="text-[11px] text-slate-500 uppercase font-semibold">Avg Usability Score</p>
                <p className="text-2xl font-bold text-indigo-400">{stakeholders?.avg_usability_rating ?? 'N/A'} / 5</p>
              </div>
              <div className="p-3 bg-slate-900 rounded-xl border border-slate-800">
                <p className="text-[11px] text-slate-500 uppercase font-semibold">Avg Explainability Score</p>
                <p className="text-2xl font-bold text-emerald-400">{stakeholders?.avg_explainability_rating ?? 'N/A'} / 5</p>
              </div>
            </div>

            <div className="p-4 bg-slate-900/40 rounded-xl border border-slate-800 text-xs space-y-2">
              <p className="font-semibold text-slate-300">Stakeholder Persona Breakdown ({stakeholders?.total_validations ?? 0} reviews):</p>
              <div className="grid grid-cols-2 gap-2">
                {stakeholders?.role_breakdown?.map((rb, idx) => (
                  <div key={idx} className="p-2 bg-slate-800/60 rounded border border-slate-700 flex justify-between">
                    <span className="text-slate-300 font-medium">{rb.role}</span>
                    <span className="font-bold text-sky-400">{rb.count} reviews</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* C5 Interactive Stakeholder Validation Modal */}
      {isValidationModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 max-w-lg w-full space-y-5 shadow-2xl animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <Users className="w-5 h-5 text-indigo-400" />
                <h3 className="text-base font-bold text-white">Stakeholder System Validation</h3>
              </div>
              <button
                onClick={() => setIsValidationModalOpen(false)}
                className="p-1 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {validationSuccess && (
              <div className="p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-xs text-emerald-300 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                <span>{validationSuccess}</span>
              </div>
            )}

            {validationError && (
              <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-xl text-xs text-red-300 flex items-center gap-2">
                <ShieldAlert className="w-4 h-4 text-red-400 flex-shrink-0" />
                <span>{validationError}</span>
              </div>
            )}

            <form onSubmit={handleValidationSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">
                  Stakeholder Role
                </label>
                <select
                  value={stakeholderRole}
                  onChange={(e) => setStakeholderRole(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
                >
                  <option value="Routing Officer">Routing Officer</option>
                  <option value="PWD Engineer">PWD Engineer</option>
                  <option value="Supervisor">Supervisor</option>
                  <option value="Citizen Evaluator">Citizen Evaluator</option>
                  <option value="External Auditor">External Auditor</option>
                </select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">
                    Usability Rating (1-5)
                  </label>
                  <select
                    value={usabilityRating}
                    onChange={(e) => setUsabilityRating(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
                  >
                    <option value="5">5 — Excellent</option>
                    <option value="4">4 — Good</option>
                    <option value="3">3 — Moderate</option>
                    <option value="2">2 — Needs Work</option>
                    <option value="1">1 — Poor</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">
                    Explainability Rating (1-5)
                  </label>
                  <select
                    value={explainabilityRating}
                    onChange={(e) => setExplainabilityRating(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
                  >
                    <option value="5">5 — Extremely Clear</option>
                    <option value="4">4 — Clear</option>
                    <option value="3">3 — Average</option>
                    <option value="2">2 — Confusing</option>
                    <option value="1">1 — Unclear</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">
                  Routing Speedup Gain %
                </label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={speedupPct}
                  onChange={(e) => setSpeedupPct(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">
                  Findings & Feedback Comments
                </label>
                <textarea
                  rows="3"
                  value={feedbackNotes}
                  onChange={(e) => setFeedbackNotes(e.target.value)}
                  placeholder="Describe your qualitative evaluation, ease of finding features, or audit feedback..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setIsValidationModalOpen(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 rounded-xl transition-colors font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submittingValidation}
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-xs text-white font-bold rounded-xl transition-all shadow-md flex items-center gap-1.5"
                >
                  {submittingValidation ? (
                    <>
                      <Loader2 className="w-3.5 h-3.5 animate-spin" />
                      <span>Submitting...</span>
                    </>
                  ) : (
                    <span>Submit Evaluation</span>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

