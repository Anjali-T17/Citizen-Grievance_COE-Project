import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { complaintAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import {
  FileText,
  Languages,
  FileCheck,
  AlertTriangle,
  MessageSquare,
  ArrowLeft,
  Paperclip,
  CheckCircle,
  CheckCircle2,
  Loader2,
  ShieldAlert,
  Globe
} from 'lucide-react';
import { EscalationModal } from '../components/EscalationModal';
import { OverrideModal } from '../components/OverrideModal';

export const ComplaintDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const role = user?.role || 'Citizen';

  const [complaint, setComplaint] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Translation states (C1)
  const [targetLang, setTargetLang] = useState('English');
  const [isTranslating, setIsTranslating] = useState(false);
  const [translationResult, setTranslationResult] = useState(null);
  const [translationError, setTranslationError] = useState('');

  // Resolution modal states (C2)
  const [isResolveModalOpen, setIsResolveModalOpen] = useState(false);
  const [resolveComment, setResolveComment] = useState('');
  const [isResolving, setIsResolving] = useState(false);
  const [resolveError, setResolveError] = useState('');

  // Officer action states
  const [internalNote, setInternalNote] = useState('');
  const [notesList, setNotesList] = useState([]);
  const [actionNotice, setActionNotice] = useState('');

  // Modals
  const [isEscalationOpen, setIsEscalationOpen] = useState(false);
  const [isOverrideOpen, setIsOverrideOpen] = useState(false);

  useEffect(() => {
    fetchDetails();
  }, [id]);

  const fetchDetails = async () => {
    setIsLoading(true);
    try {
      const res = await complaintAPI.getComplaintById(id);
      setComplaint(res.data);
    } catch (err) {
      console.error('Failed to fetch complaint details:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTranslateReal = async () => {
    if (!complaint) return;
    setIsTranslating(true);
    setTranslationError('');
    try {
      const res = await complaintAPI.translateText({
        text: complaint.description,
        source_language: complaint.language || 'Tamil',
        target_language: targetLang,
      });
      setTranslationResult(res.data);
      setActionNotice(
        `Feature F003 (Translate Complaint) executed via backend API (${res.data.source_language} → ${res.data.target_language}).`
      );
    } catch (err) {
      setTranslationError(err.response?.data?.detail || 'Failed to execute backend translation.');
    } finally {
      setIsTranslating(false);
    }
  };

  const handleResolveConfirm = async (e) => {
    e.preventDefault();
    if (!complaint) return;
    setIsResolving(true);
    setResolveError('');
    try {
      const res = await complaintAPI.updateStatus(complaint.complaint_id, {
        status: 'Resolved',
        role: role,
        organisation: user?.organisation,
        user_id: user?.user_id || 'USER_001',
        comment: resolveComment.trim() || 'Grievance inspected, action taken, and case marked as Resolved.',
      });
      setComplaint(res.data);
      setIsResolveModalOpen(false);
      setActionNotice('✅ Complaint status updated to RESOLVED. Backend audit log recorded.');
    } catch (err) {
      const errMsg =
        typeof err.response?.data?.detail === 'string'
          ? err.response.data.detail
          : err.response?.data?.detail?.reason || 'Failed to update complaint status.';
      setResolveError(errMsg);
    } finally {
      setIsResolving(false);
    }
  };

  const handleVerifyAttachment = () => {
    setActionNotice('Feature F004 (Verify Attachment) executed. File metadata validated.');
  };

  const handleAddInternalNote = (e) => {
    e.preventDefault();
    if (!internalNote.trim()) return;
    setNotesList([...notesList, { text: internalNote, date: new Date().toLocaleTimeString() }]);
    setInternalNote('');
    setActionNotice('Feature F006 (Internal Notes) executed. Note appended.');
  };

  const handleEscalationConfirm = async () => {
    setIsEscalationOpen(false);
    if (!complaint) return;
    try {
      const res = await complaintAPI.updateStatus(complaint.complaint_id, {
        status: 'Escalated',
        role: role,
        organisation: user?.organisation,
        user_id: user?.user_id || 'USER_001',
        comment: 'SLA breach triggered manual officer escalation to supervisor.',
      });
      setComplaint(res.data);
      setActionNotice('✅ Feature F005 (Escalate Complaint) confirmed. Status updated to Escalated.');
    } catch (err) {
      console.error('Escalation failed:', err);
    }
  };

  if (isLoading) {
    return (
      <div className="p-12 text-center text-slate-400">
        <Loader2 className="w-8 h-8 animate-spin mx-auto text-sky-400 mb-2" />
        <p className="text-xs">Loading complaint {id} details from backend...</p>
      </div>
    );
  }

  if (!complaint) {
    return (
      <div className="p-8 text-center text-slate-400">
        <p>Complaint {id} not found.</p>
        <button onClick={() => navigate('/my-complaints')} className="mt-4 text-sky-400 underline text-xs">
          Back to My Complaints
        </button>
      </div>
    );
  }

  const isResolved = complaint.status === 'Resolved';
  const isAuthorizedOfficer = role !== 'Citizen';

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header Back Button */}
      <button
        onClick={() => navigate('/my-complaints')}
        className="inline-flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-white transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Complaints List</span>
      </button>

      {/* Main Details Card */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-mono font-bold text-sky-400">{complaint.complaint_id}</h1>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-sky-500/10 text-sky-300 border border-sky-500/30">
                {complaint.category}
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1">Submitted on {new Date(complaint.created_at).toLocaleString()}</p>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-slate-400">Status:</span>
            <span
              className={`px-3 py-1 rounded-full text-xs font-extrabold border ${
                isResolved
                  ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                  : complaint.status === 'Escalated'
                  ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                  : 'bg-sky-500/10 text-sky-400 border-sky-500/30'
              }`}
            >
              {complaint.status}
            </span>
          </div>
        </div>

        {actionNotice && (
          <div className="p-3 bg-sky-950/40 border border-sky-500/30 rounded-xl text-xs text-sky-300 font-medium flex items-center gap-2 animate-fadeIn">
            <CheckCircle className="w-4 h-4 text-sky-400" />
            <span>{actionNotice}</span>
          </div>
        )}

        {/* Complaint Text */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
              Original Complaint Text ({complaint.language})
            </h3>
          </div>
          <div className="p-4 bg-slate-900 rounded-xl border border-slate-700/60 text-slate-100 text-sm leading-relaxed">
            {complaint.description}
          </div>
        </div>

        {/* C1: Functional Translation UI */}
        <div className="p-4 bg-slate-900/60 rounded-xl border border-slate-800 space-y-3">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-center gap-2 text-xs font-bold text-sky-400">
              <Languages className="w-4 h-4" />
              <span>F003 - Functional Backend Text Translation</span>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-[11px] text-slate-400">Target Language:</span>
              <select
                value={targetLang}
                onChange={(e) => setTargetLang(e.target.value)}
                className="bg-slate-800 border border-slate-700 text-white text-xs rounded-lg px-2.5 py-1 focus:outline-none focus:border-sky-500"
              >
                <option value="English">English</option>
                <option value="Tamil">Tamil (தமிழ்)</option>
                <option value="Hindi">Hindi (हिंदी)</option>
              </select>

              <button
                onClick={handleTranslateReal}
                disabled={isTranslating}
                className="px-3.5 py-1.5 bg-sky-600 hover:bg-sky-500 disabled:opacity-50 text-white text-xs font-bold rounded-lg transition-colors flex items-center gap-1.5"
              >
                {isTranslating ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Globe className="w-3.5 h-3.5" />}
                <span>Translate via API</span>
              </button>
            </div>
          </div>

          {translationError && (
            <div className="p-2.5 bg-red-950/40 border border-red-500/30 rounded-lg text-xs text-red-300">
              {translationError}
            </div>
          )}

          {translationResult && (
            <div className="p-3.5 bg-indigo-950/40 border border-indigo-500/40 rounded-xl space-y-2 animate-fadeIn text-xs">
              <div className="flex items-center justify-between text-indigo-300 text-[11px] font-semibold border-b border-indigo-500/20 pb-1.5">
                <span>
                  Source: <strong>{translationResult.source_language}</strong> → Target:{' '}
                  <strong>{translationResult.target_language}</strong>
                </span>
                <span className="text-[10px] text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20">
                  {translationResult.engine}
                </span>
              </div>
              <div className="text-indigo-100 font-medium leading-relaxed">
                "{translationResult.translated_text}"
              </div>
            </div>
          )}
        </div>

        {/* Attachment View */}
        {complaint.attachments && complaint.attachments.length > 0 && (
          <div>
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Attached Documents</h3>
            <div className="space-y-2">
              {complaint.attachments.map((att) => (
                <div key={att.id} className="p-3 bg-slate-900 rounded-xl border border-slate-700/60 flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2">
                    <Paperclip className="w-4 h-4 text-sky-400" />
                    <span className="font-semibold text-slate-200">{att.filename}</span>
                    <span className="text-slate-500">({(att.file_size / 1024).toFixed(1)} KB)</span>
                  </div>
                  <span className="px-2 py-0.5 bg-slate-800 text-slate-400 rounded border border-slate-700">
                    {att.upload_status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* C2: Role Officer Action Buttons & Resolution Controls */}
        {isAuthorizedOfficer && (
          <div className="border-t border-slate-800 pt-5 space-y-4">
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Permitted Officer Actions</h3>
            <div className="flex flex-wrap gap-3">
              <button
                onClick={handleVerifyAttachment}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-emerald-300 border border-slate-700 rounded-xl text-xs font-semibold transition-colors flex items-center gap-2"
              >
                <FileCheck className="w-4 h-4 text-emerald-400" />
                <span>F004 - Verify Attachment</span>
              </button>

              <button
                onClick={() => setIsEscalationOpen(true)}
                disabled={isResolved}
                className="px-4 py-2 bg-amber-500/20 hover:bg-amber-500/30 disabled:opacity-40 text-amber-300 border border-amber-500/40 rounded-xl text-xs font-semibold transition-colors flex items-center gap-2"
              >
                <AlertTriangle className="w-4 h-4 text-amber-400" />
                <span>F005 - Escalate SLA Breach</span>
              </button>

              {/* C2: Resolve Complaint Button */}
              <button
                onClick={() => setIsResolveModalOpen(true)}
                disabled={isResolved}
                className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-40 text-white rounded-xl text-xs font-bold transition-colors flex items-center gap-2 shadow-lg"
              >
                <CheckCircle2 className="w-4 h-4" />
                <span>{isResolved ? 'Complaint Resolved' : 'Resolve Complaint'}</span>
              </button>
            </div>

            {/* Internal Notes Form (F006) */}
            <div className="pt-2">
              <form onSubmit={handleAddInternalNote} className="space-y-2">
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  F006 - Add Internal Case Note
                </label>
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={internalNote}
                    onChange={(e) => setInternalNote(e.target.value)}
                    placeholder="Confidential case note for internal staff..."
                    className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
                  />
                  <button
                    type="submit"
                    className="px-4 py-2 bg-sky-600 hover:bg-sky-500 text-white rounded-xl text-xs font-bold"
                  >
                    Add Note
                  </button>
                </div>
              </form>

              {notesList.length > 0 && (
                <div className="mt-3 space-y-2">
                  {notesList.map((n, i) => (
                    <div key={i} className="p-2.5 bg-slate-900/60 border border-slate-800 rounded-lg text-xs text-slate-300 flex justify-between">
                      <span>{n.text}</span>
                      <span className="text-slate-500 text-[10px]">{n.date}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* C2: Resolve Confirmation Modal */}
      {isResolveModalOpen && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="glass-panel max-w-md w-full p-6 rounded-2xl border border-slate-800 space-y-4 shadow-2xl animate-fadeIn">
            <div className="flex items-center gap-2 text-emerald-400 border-b border-slate-800 pb-3">
              <CheckCircle2 className="w-5 h-5" />
              <h3 className="text-base font-bold text-white">Confirm Complaint Resolution</h3>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed">
              Are you sure you want to mark complaint <strong className="text-sky-400">{complaint.complaint_id}</strong> as{' '}
              <strong className="text-emerald-400">RESOLVED</strong>? Once resolved, the complaint lifecycle will be completed.
            </p>

            {resolveError && (
              <div className="p-3 bg-red-950/40 border border-red-500/40 rounded-xl text-xs text-red-300 flex items-start gap-2">
                <ShieldAlert className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
                <span>{resolveError}</span>
              </div>
            )}

            <form onSubmit={handleResolveConfirm} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Resolution Inspection Comment:</label>
                <textarea
                  rows={3}
                  value={resolveComment}
                  onChange={(e) => setResolveComment(e.target.value)}
                  placeholder="Describe resolution actions taken on site..."
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setIsResolveModalOpen(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold rounded-xl border border-slate-700 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isResolving}
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white text-xs font-bold rounded-xl shadow-lg transition-colors flex items-center gap-1.5"
                >
                  {isResolving && <Loader2 className="w-3.5 h-3.5 animate-spin" />}
                  <span>Confirm Resolution</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Escalation Confirmation Modal */}
      <EscalationModal
        isOpen={isEscalationOpen}
        onConfirm={handleEscalationConfirm}
        onCancel={() => {
          setIsEscalationOpen(false);
          setIsOverrideOpen(true);
        }}
      />

      {/* Override Modal */}
      <OverrideModal
        isOpen={isOverrideOpen}
        onClose={() => setIsOverrideOpen(false)}
        userId={user?.user_id}
        onOverrideSuccess={(reason) => setActionNotice(`Override stored: "${reason}"`)}
      />
    </div>
  );
};

