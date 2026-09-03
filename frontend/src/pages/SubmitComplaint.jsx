import React, { useState } from 'react';
import { complaintAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { FilePlus, Upload, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const SubmitComplaint = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [description, setDescription] = useState('');
  const [language, setLanguage] = useState('English');
  const [category, setCategory] = useState('Public Safety');
  const [priority, setPriority] = useState('High');
  const [file, setFile] = useState(null);

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submittedComplaint, setSubmittedComplaint] = useState(null);
  const [error, setError] = useState('');

  const handleSampleFill = (lang) => {
    setLanguage(lang);
    if (lang === 'Tamil') {
      setDescription('தெரு விளக்கு எரியவில்லை. இரவில் மக்கள் செல்வது ஆபத்தாக உள்ளது.');
      setCategory('Public Safety');
      setPriority('High');
    } else if (lang === 'Hindi') {
      setDescription('हमारे इलाके में पीने के पानी की आपूर्ति पिछले 3 दिनों से बंद है।');
      setCategory('Water Supply');
      setPriority('Medium');
    } else {
      setDescription('Pothole on Main Road near Central Bus Terminal causing vehicle damages.');
      setCategory('Roads');
      setPriority('High');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!description.trim()) {
      setError('Please provide complaint description text.');
      return;
    }

    setIsSubmitting(true);
    setError('');
    try {
      const payload = {
        description,
        language,
        category,
        priority,
        attachment_name: file ? file.name : null,
        attachment_type: file ? file.type : null,
        attachment_size: file ? file.size : 0,
      };

      const res = await complaintAPI.createComplaint(payload, user?.user_id || 'USER_001');
      setSubmittedComplaint(res.data);
    } catch (err) {
      console.error('Failed to submit complaint:', err);
      setError('Failed to submit complaint through FastAPI backend.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Title Banner */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-2xl font-black text-white flex items-center gap-2.5">
            <FilePlus className="w-6 h-6 text-sky-400" />
            <span>Submit Citizen Grievance</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Multilingual complaint submission endpoint connected to SQLite database
          </p>
        </div>

        {/* Preset Sample Fillers */}
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400 font-semibold">Demo Multilingual Fill:</span>
          <button
            type="button"
            onClick={() => handleSampleFill('Tamil')}
            className="text-xs px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-sky-300 rounded border border-slate-700"
          >
            Tamil
          </button>
          <button
            type="button"
            onClick={() => handleSampleFill('Hindi')}
            className="text-xs px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-purple-300 rounded border border-slate-700"
          >
            Hindi
          </button>
          <button
            type="button"
            onClick={() => handleSampleFill('English')}
            className="text-xs px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded border border-slate-700"
          >
            English
          </button>
        </div>
      </div>

      {submittedComplaint ? (
        <div className="glass-panel p-8 rounded-3xl border border-emerald-500/40 text-center space-y-4 shadow-2xl animate-fadeIn">
          <CheckCircle2 className="w-16 h-16 text-emerald-400 mx-auto" />
          <h2 className="text-2xl font-extrabold text-white">Complaint Submitted Successfully!</h2>
          <p className="text-sm text-slate-300">
            Your grievance has been stored in the database with Anonymous Tracking ID:
          </p>
          <div className="inline-block px-6 py-2.5 bg-slate-800 border border-emerald-500/40 rounded-xl text-xl font-mono font-bold text-emerald-400 shadow-inner">
            {submittedComplaint.complaint_id}
          </div>

          <div className="pt-4 flex justify-center gap-4">
            <button
              onClick={() => setSubmittedComplaint(null)}
              className="px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-white text-sm font-semibold rounded-xl"
            >
              Submit Another Complaint
            </button>
            <button
              onClick={() => navigate('/my-complaints')}
              className="px-5 py-2.5 bg-sky-500 hover:bg-sky-400 text-slate-950 text-sm font-bold rounded-xl"
            >
              View in My Complaints
            </button>
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-5">
          {error && (
            <div className="p-3 bg-red-950/40 border border-red-500/40 rounded-xl text-xs text-red-300 flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-red-400" />
              <span>{error}</span>
            </div>
          )}

          {/* Language & Category */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Complaint Language
              </label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-sky-500"
              >
                <option value="English">English</option>
                <option value="Tamil">Tamil (தமிழ்)</option>
                <option value="Hindi">Hindi (हिंदी)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Category
              </label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-sky-500"
              >
                <option value="Public Safety">Public Safety / Street Lights</option>
                <option value="Water Supply">Water Supply & Sanitation</option>
                <option value="Roads">Roads & Traffic</option>
                <option value="Electricity">Electricity Grid</option>
                <option value="Waste Management">Waste Management</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Priority Level
              </label>
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-sky-500"
              >
                <option value="Low">Low Priority</option>
                <option value="Medium">Medium Priority</option>
                <option value="High">High Priority (Urgent)</option>
              </select>
            </div>
          </div>

          {/* Description */}
          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              Grievance Description
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={4}
              placeholder="Describe your complaint clearly..."
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
            />
          </div>

          {/* Attachment Upload */}
          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              Supporting Attachment (Photo / Document)
            </label>
            <div className="border-2 border-dashed border-slate-700 hover:border-sky-500 rounded-xl p-4 text-center cursor-pointer transition-colors bg-slate-900/50">
              <input
                type="file"
                id="file-upload"
                onChange={(e) => setFile(e.target.files[0])}
                className="hidden"
              />
              <label htmlFor="file-upload" className="cursor-pointer space-y-1 block">
                <Upload className="w-6 h-6 text-sky-400 mx-auto" />
                <p className="text-xs text-slate-300 font-medium">
                  {file ? file.name : 'Click to select photo proof (JPEG/PNG/PDF)'}
                </p>
                {file && <p className="text-[11px] text-emerald-400">({(file.size / 1024).toFixed(1)} KB)</p>}
              </label>
            </div>
          </div>

          {/* Submit Action */}
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full py-3.5 bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-400 hover:to-blue-500 text-white font-extrabold rounded-xl text-sm transition-all shadow-xl shadow-sky-500/20 flex items-center justify-center gap-2"
          >
            {isSubmitting ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Saving to Database...</span>
              </>
            ) : (
              <span>Submit Complaint</span>
            )}
          </button>
        </form>
      )}
    </div>
  );
};
