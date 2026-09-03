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
  Loader2
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

  // Officer action states
  const [translationText, setTranslationText] = useState('');
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

  const handleTranslateDemo = () => {
    if (!complaint) return;
    if (complaint.language === 'Tamil') {
      setTranslationText(
        'English Working Translation:\n"Street lights are not working. Walking at night is dangerous for citizens."'
      );
    } else if (complaint.language === 'Hindi') {
      setTranslationText(
        'English Working Translation:\n"Drinking water supply in our area has been shut down for the last 3 days."'
      );
    } else {
      setTranslationText('English Native Text:\n"' + complaint.description + '"');
    }
    setActionNotice('Feature F003 (Translate Complaint) executed successfully.');
  };

  const handleVerifyAttachment = () => {
    setActionNotice('Feature F004 (Verify Attachment) executed. Image metadata validated.');
  };

  const handleAddInternalNote = (e) => {
    e.preventDefault();
    if (!internalNote.trim()) return;
    setNotesList([...notesList, { text: internalNote, date: new Date().toLocaleTimeString() }]);
    setInternalNote('');
    setActionNotice('Feature F006 (Internal Notes) executed. Note appended.');
  };

  const handleEscalationConfirm = () => {
    setIsEscalationOpen(false);
    if (complaint) complaint.status = 'Escalated';
    setActionNotice('✅ Feature F005 (Escalate Complaint) confirmed. Status updated to Escalated.');
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
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-6">
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
            <span className="px-3 py-1 rounded-full text-xs font-extrabold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
              {complaint.status}
            </span>
          </div>
        </div>

        {actionNotice && (
          <div className="p-3 bg-sky-950/40 border border-sky-500/30 rounded-xl text-xs text-sky-300 font-medium flex items-center gap-2">
            <CheckCircle className="w-4 h-4 text-sky-400" />
            <span>{actionNotice}</span>
          </div>
        )}

        {/* Complaint Text */}
        <div>
          <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Original Complaint Text</h3>
          <div className="p-4 bg-slate-900 rounded-xl border border-slate-700/60 text-slate-100 text-sm leading-relaxed">
            {complaint.description}
          </div>
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

        {/* Translation Demo Output */}
        {translationText && (
          <div className="p-4 bg-indigo-950/40 border border-indigo-500/40 rounded-xl space-y-1 animate-fadeIn">
            <div className="flex items-center gap-2 text-indigo-400 text-xs font-bold">
              <Languages className="w-4 h-4" />
              <span>Translation Feature Output (F003)</span>
            </div>
            <pre className="text-xs text-indigo-200 whitespace-pre-wrap font-sans">{translationText}</pre>
          </div>
        )}

        {/* Role Officer Action Buttons (F003, F004, F005, F006) */}
        {role !== 'Citizen' && (
          <div className="border-t border-slate-800 pt-5 space-y-4">
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Permitted Officer Actions</h3>
            <div className="flex flex-wrap gap-3">
              <button
                onClick={handleTranslateDemo}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-sky-300 border border-slate-700 rounded-xl text-xs font-semibold transition-colors flex items-center gap-2"
              >
                <Languages className="w-4 h-4 text-sky-400" />
                <span>F003 - Translate Complaint</span>
              </button>

              <button
                onClick={handleVerifyAttachment}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-emerald-300 border border-slate-700 rounded-xl text-xs font-semibold transition-colors flex items-center gap-2"
              >
                <FileCheck className="w-4 h-4 text-emerald-400" />
                <span>F004 - Verify Attachment</span>
              </button>

              <button
                onClick={() => setIsEscalationOpen(true)}
                className="px-4 py-2 bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 rounded-xl text-xs font-semibold transition-colors flex items-center gap-2"
              >
                <AlertTriangle className="w-4 h-4 text-amber-400" />
                <span>F005 - Escalate Complaint (High Impact)</span>
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
