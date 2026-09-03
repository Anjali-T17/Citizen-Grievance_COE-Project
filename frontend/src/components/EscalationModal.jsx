import React from 'react';
import { AlertTriangle, ShieldCheck, X } from 'lucide-react';

export const EscalationModal = ({ isOpen, onConfirm, onCancel }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-sm animate-fadeIn">
      <div className="bg-slate-900 border border-amber-500/40 rounded-2xl w-full max-w-lg shadow-2xl shadow-amber-500/10 overflow-hidden">
        {/* Banner Header */}
        <div className="p-5 bg-gradient-to-r from-amber-500/20 to-orange-500/20 border-b border-amber-500/30 flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-amber-500/20 text-amber-400 border border-amber-500/40">
            <AlertTriangle className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-amber-300">⚠️ Escalation Recommended</h3>
            <p className="text-xs text-amber-200/80">High-Impact System Action Requires Human Confirmation</p>
          </div>
        </div>

        {/* Content Body */}
        <div className="p-6 space-y-4">
          <div className="p-3.5 bg-slate-800/60 rounded-xl border border-slate-700/60 text-xs text-slate-300 space-y-2">
            <p className="font-semibold text-slate-200">Assistant Evaluation Trigger Factors:</p>
            <ul className="list-disc list-inside space-y-1 text-slate-400">
              <li>High priority / SLA breach condition identified</li>
              <li>Escalation feature permitted for your role (Grievance Officer / Supervisor)</li>
              <li>Underused high-impact workflow feature</li>
            </ul>
          </div>

          <div className="p-4 bg-amber-950/30 border border-amber-500/30 rounded-xl text-center space-y-1">
            <ShieldCheck className="w-6 h-6 text-amber-400 mx-auto" />
            <h4 className="text-sm font-bold text-white">Human Confirmation Required</h4>
            <p className="text-xs text-slate-300">
              Are you sure you want to escalate this complaint to Senior Supervisor Authorities?
            </p>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="px-6 py-4 bg-slate-800/40 border-t border-slate-800 flex items-center justify-end gap-3">
          <button
            onClick={onCancel}
            className="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-sm font-medium transition-colors"
          >
            Cancel & Override
          </button>
          <button
            onClick={onConfirm}
            className="px-5 py-2.5 bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold rounded-lg text-sm transition-colors shadow-lg shadow-amber-500/20"
          >
            Confirm Escalation
          </button>
        </div>
      </div>
    </div>
  );
};
