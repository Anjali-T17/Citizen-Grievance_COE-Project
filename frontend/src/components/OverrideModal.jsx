import React, { useState } from 'react';
import { HelpCircle, X, Check } from 'lucide-react';
import { overrideAPI } from '../services/api';

export const OverrideModal = ({ isOpen, onClose, recommendation, userId = 'USER_001', onOverrideSuccess }) => {
  const [reason, setReason] = useState('Not urgent');
  const [comment, setComment] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await overrideAPI.recordOverride({
        recommendation_id: recommendation?.id || 1,
        anonymous_user_id: userId,
        action: 'CANCEL_RECOMMENDATION',
        override_reason: reason,
        comment: comment,
      });
      if (onOverrideSuccess) onOverrideSuccess(reason);
      onClose();
    } catch (err) {
      console.error('Failed to submit override:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-sm animate-fadeIn">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-800/40">
          <div className="flex items-center gap-2">
            <HelpCircle className="w-5 h-5 text-indigo-400" />
            <h3 className="text-lg font-bold text-white">Capture Override Reason</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <p className="text-sm text-slate-300">
            Why are you overriding this feature recommendation?
          </p>

          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              Select Override Reason
            </label>
            <select
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-sky-500"
            >
              <option value="Not urgent">Not urgent</option>
              <option value="Wrong recommendation">Wrong recommendation</option>
              <option value="Already handled">Already handled</option>
              <option value="Permission/ownership issue">Permission/ownership issue</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              Additional Context / Comments (Optional)
            </label>
            <textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              rows={3}
              placeholder="Provide brief context for system audit logs..."
              className="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
            />
          </div>

          <div className="pt-3 flex justify-end gap-3 border-t border-slate-800">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-slate-400 hover:text-white text-sm font-medium"
            >
              Close
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-lg text-sm transition-colors flex items-center gap-2"
            >
              <Check className="w-4 h-4" />
              <span>{isSubmitting ? 'Saving...' : 'Save Reason'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
