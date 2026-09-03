import React from 'react';
import { X, CheckCircle2, XCircle, Award, HelpCircle } from 'lucide-react';

export const EvidenceModal = ({ isOpen, onClose, recommendation }) => {
  if (!isOpen || !recommendation) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fadeIn">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-xl shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-800/40">
          <div className="flex items-center gap-2">
            <Award className="w-5 h-5 text-sky-400" />
            <h3 className="text-lg font-bold text-white">Why This Recommendation?</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6 max-h-[80vh] overflow-y-auto">
          {/* Feature & Score Banner */}
          <div className="p-4 rounded-xl bg-slate-800/60 border border-slate-700/60 flex items-center justify-between">
            <div>
              <span className="text-xs font-semibold text-sky-400 uppercase tracking-wider">Recommended Feature</span>
              <h4 className="text-xl font-bold text-white">{recommendation.feature_name}</h4>
              <p className="text-xs text-slate-400 mt-0.5">{recommendation.description}</p>
            </div>
            <div className="text-right">
              <div className="text-2xl font-black text-emerald-400">{recommendation.score} <span className="text-xs text-slate-400 font-normal">/ 100</span></div>
              <span className="inline-block mt-1 text-[11px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                Transparent Rule Score
              </span>
            </div>
          </div>

          {/* Rule Breakdown List */}
          <div>
            <h5 className="text-xs font-semibold uppercase text-slate-400 tracking-wider mb-3">Scoring Engine Rule Matches</h5>
            <div className="space-y-2">
              {recommendation.matched_rules?.map((rule, idx) => (
                <div
                  key={idx}
                  className={`p-3 rounded-lg border flex items-start justify-between ${
                    rule.matched
                      ? 'bg-slate-800/40 border-slate-700/70 text-slate-200'
                      : 'bg-slate-900/40 border-slate-800 text-slate-500'
                  }`}
                >
                  <div className="flex items-start gap-2.5">
                    {rule.matched ? (
                      <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                    ) : (
                      <XCircle className="w-5 h-5 text-slate-600 shrink-0 mt-0.5" />
                    )}
                    <div>
                      <p className="text-sm font-semibold">{rule.rule_name}</p>
                      <p className="text-xs opacity-80 mt-0.5">{rule.explanation}</p>
                    </div>
                  </div>
                  <span className={`text-xs font-bold px-2 py-0.5 rounded ${rule.matched ? 'bg-emerald-500/20 text-emerald-300' : 'bg-slate-800 text-slate-500'}`}>
                    +{rule.points} pts
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Explicit Evidence List */}
          <div>
            <h5 className="text-xs font-semibold uppercase text-slate-400 tracking-wider mb-2">Evidence Trail</h5>
            <ul className="space-y-1.5 pl-2">
              {recommendation.evidence?.map((ev, i) => (
                <li key={i} className="text-xs text-sky-300 flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-sky-400"></span>
                  <span>{ev}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-3 bg-slate-800/40 border-t border-slate-800 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg text-sm font-medium transition-colors"
          >
            Close Explanation
          </button>
        </div>
      </div>
    </div>
  );
};
