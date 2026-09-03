import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Building2, UserCheck, ShieldAlert, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const Navbar = () => {
  const { user, login } = useAuth();
  const navigate = useNavigate();

  const handleRoleSwitch = async (e) => {
    const val = e.target.value;
    if (val === 'Citizen') await login('Municipal Corporation', 'Citizen');
    else if (val === 'Grievance Officer') await login('Municipal Corporation', 'Grievance Officer');
    else if (val === 'Supervisor') await login('Municipal Corporation', 'Supervisor');
    else if (val === 'External Partner') await login('External Partner', 'External Partner');
    else if (val === 'Field Inspector') await login('Public Works Department', 'Field Inspector');
    else if (val === 'SLA Auditor') await login('Municipal Corporation', 'SLA Auditor');
    navigate('/');
  };

  return (
    <header className="h-16 bg-slate-900 border-b border-slate-800 px-6 flex items-center justify-between sticky top-0 z-40 shadow-lg">
      <div className="flex items-center gap-3">
        <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-500/20">
          <Building2 className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="text-lg font-bold text-white tracking-wide">Citizen Grievance COE</h1>
          <p className="text-xs text-sky-400 font-medium">Role-Aware Feature Discovery Engine (100% Full System)</p>
        </div>
      </div>

      {user && (
        <div className="flex items-center gap-4">
          <div className="hidden md:flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-800 border border-slate-700 text-xs text-slate-300">
            <Building2 className="w-3.5 h-3.5 text-sky-400" />
            <span>{user.organisation}</span>
          </div>

          <div className="flex items-center gap-2 bg-slate-800/80 border border-slate-700/80 rounded-lg p-1">
            <UserCheck className="w-4 h-4 text-emerald-400 ml-2" />
            <select
              value={user.role}
              onChange={handleRoleSwitch}
              className="bg-transparent text-xs font-semibold text-white focus:outline-none cursor-pointer pr-2"
            >
              <option value="Citizen" className="bg-slate-800">Citizen (Municipal Corp)</option>
              <option value="Grievance Officer" className="bg-slate-800">Grievance Officer (Municipal Corp)</option>
              <option value="Supervisor" className="bg-slate-800">Supervisor (Municipal Corp)</option>
              <option value="External Partner" className="bg-slate-800">External Partner Agency</option>
              <option value="Field Inspector" className="bg-slate-800">Field Inspector (PWD)</option>
              <option value="SLA Auditor" className="bg-slate-800">SLA Auditor (Municipal Corp)</option>
            </select>
          </div>

          <div className="flex items-center gap-2 pl-2 border-l border-slate-800">
            <div className="w-8 h-8 rounded-full bg-indigo-600/30 border border-indigo-500/40 text-indigo-300 font-semibold text-xs flex items-center justify-center">
              {user.user_id}
            </div>
          </div>
        </div>
      )}
    </header>
  );
};
