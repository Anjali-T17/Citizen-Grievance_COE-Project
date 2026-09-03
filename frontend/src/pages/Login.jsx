import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Building2, Shield, UserCheck, ArrowRight, HardHat, FileSearch } from 'lucide-react';

export const Login = () => {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [organisation, setOrganisation] = useState('Municipal Corporation');
  const [role, setRole] = useState('Citizen');

  const handleOrgChange = (org) => {
    setOrganisation(org);
    if (org === 'External Partner') setRole('External Partner');
    else if (org === 'Public Works Department') setRole('Field Inspector');
    else if (org === 'Public Health & Sanitation') setRole('Citizen');
    else setRole('Citizen');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await login(organisation, role);
    navigate('/');
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center p-6 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-800 via-slate-900 to-slate-950">
      <div className="w-full max-w-lg glass-panel p-8 rounded-3xl border border-slate-800 shadow-2xl space-y-6">
        <div className="text-center space-y-2">
          <div className="h-14 w-14 rounded-2xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center mx-auto shadow-xl shadow-sky-500/25">
            <Building2 className="w-8 h-8 text-white" />
          </div>
          <h2 className="text-2xl font-black text-white">Full System Prototype Access</h2>
          <p className="text-xs text-slate-400">Select Organisation and Role context to launch session</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Select Organisation */}
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              1. Select Organisation
            </label>
            <div className="grid grid-cols-2 gap-2.5">
              <button
                type="button"
                onClick={() => handleOrgChange('Municipal Corporation')}
                className={`p-3 rounded-xl border text-left text-xs font-semibold transition-all ${
                  organisation === 'Municipal Corporation'
                    ? 'bg-sky-500/20 border-sky-500 text-sky-300 shadow-lg shadow-sky-500/10'
                    : 'bg-slate-800/60 border-slate-700/80 text-slate-400 hover:border-slate-600'
                }`}
              >
                <Building2 className="w-4 h-4 mb-1 text-sky-400" />
                <p>Municipal Corp</p>
              </button>

              <button
                type="button"
                onClick={() => handleOrgChange('Public Works Department')}
                className={`p-3 rounded-xl border text-left text-xs font-semibold transition-all ${
                  organisation === 'Public Works Department'
                    ? 'bg-amber-500/20 border-amber-500 text-amber-300 shadow-lg shadow-amber-500/10'
                    : 'bg-slate-800/60 border-slate-700/80 text-slate-400 hover:border-slate-600'
                }`}
              >
                <HardHat className="w-4 h-4 mb-1 text-amber-400" />
                <p>Public Works (PWD)</p>
              </button>

              <button
                type="button"
                onClick={() => handleOrgChange('External Partner')}
                className={`p-3 rounded-xl border text-left text-xs font-semibold transition-all ${
                  organisation === 'External Partner'
                    ? 'bg-purple-500/20 border-purple-500 text-purple-300 shadow-lg shadow-purple-500/10'
                    : 'bg-slate-800/60 border-slate-700/80 text-slate-400 hover:border-slate-600'
                }`}
              >
                <Shield className="w-4 h-4 mb-1 text-purple-400" />
                <p>External Partner</p>
              </button>

              <button
                type="button"
                onClick={() => handleOrgChange('Public Health & Sanitation')}
                className={`p-3 rounded-xl border text-left text-xs font-semibold transition-all ${
                  organisation === 'Public Health & Sanitation'
                    ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 shadow-lg shadow-emerald-500/10'
                    : 'bg-slate-800/60 border-slate-700/80 text-slate-400 hover:border-slate-600'
                }`}
              >
                <FileSearch className="w-4 h-4 mb-1 text-emerald-400" />
                <p>Health & Sanitation</p>
              </button>
            </div>
          </div>

          {/* Select Role */}
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              2. Select User Role
            </label>
            <div className="space-y-2">
              {[
                { r: 'Citizen', desc: 'Submit complaints, track status, survey feedback' },
                { r: 'Grievance Officer', desc: 'Translate text, verify documents, escalate complaints' },
                { r: 'Supervisor', desc: 'Department metrics, escalation review, SLA reports' },
                { r: 'Field Inspector', desc: 'Onsite verification, geotagged inspection reports' },
                { r: 'SLA Auditor', desc: 'SLA breach audits, bottleneck compliance analysis' },
                { r: 'External Partner', desc: 'Upload resolution proof and evidence photos' },
              ].map((item) => (
                <button
                  key={item.r}
                  type="button"
                  onClick={() => setRole(item.r)}
                  className={`w-full p-2.5 rounded-xl border text-left transition-all ${
                    role === item.r
                      ? 'bg-indigo-600/20 border-indigo-500 text-white shadow-md'
                      : 'bg-slate-800/40 border-slate-700/60 text-slate-400 hover:bg-slate-800'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-200">{item.r}</span>
                    {role === item.r && <UserCheck className="w-3.5 h-3.5 text-emerald-400" />}
                  </div>
                  <p className="text-[11px] text-slate-400 mt-0.5">{item.desc}</p>
                </button>
              ))}
            </div>
          </div>

          <button
            type="submit"
            className="w-full py-3.5 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-bold rounded-xl text-sm transition-all shadow-xl shadow-sky-500/20 flex items-center justify-center gap-2"
          >
            <span>Launch Dashboard as {role} ({organisation})</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
};
