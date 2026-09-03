import React, { useState, useEffect } from 'react';
import { complaintAPI } from '../services/api';
import { History, Eye, Search, Filter, Loader2, FileText } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const ComplaintHistory = () => {
  const [complaints, setComplaints] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchFilter, setSearchFilter] = useState('');
  const [langFilter, setLangFilter] = useState('ALL');
  const navigate = useNavigate();

  useEffect(() => {
    fetchComplaints();
  }, []);

  const fetchComplaints = async () => {
    setIsLoading(true);
    try {
      const res = await complaintAPI.getComplaints();
      setComplaints(res.data);
    } catch (err) {
      console.error('Failed to fetch complaints:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const filteredComplaints = complaints.filter((c) => {
    const matchesSearch =
      c.complaint_id.toLowerCase().includes(searchFilter.toLowerCase()) ||
      c.category.toLowerCase().includes(searchFilter.toLowerCase()) ||
      c.description.toLowerCase().includes(searchFilter.toLowerCase());
    const matchesLang = langFilter === 'ALL' || c.language === langFilter;
    return matchesSearch && matchesLang;
  });

  return (
    <div className="space-y-6">
      {/* Title & Filters */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-2xl font-black text-white flex items-center gap-2.5">
            <History className="w-6 h-6 text-sky-400" />
            <span>Complaint History & Tracking</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">Live complaints fetched from SQLite database</p>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              value={searchFilter}
              onChange={(e) => setSearchFilter(e.target.value)}
              placeholder="Search by ID or Category..."
              className="bg-slate-900 border border-slate-700 rounded-xl pl-9 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
            />
          </div>

          <select
            value={langFilter}
            onChange={(e) => setLangFilter(e.target.value)}
            className="bg-slate-900 border border-slate-700 rounded-xl px-3 py-1.5 text-xs text-white focus:outline-none focus:border-sky-500"
          >
            <option value="ALL">All Languages</option>
            <option value="English">English</option>
            <option value="Tamil">Tamil (தமிழ்)</option>
            <option value="Hindi">Hindi (हिंदी)</option>
          </select>
        </div>
      </div>

      {/* Complaints Table */}
      {isLoading ? (
        <div className="p-12 text-center text-slate-400">
          <Loader2 className="w-8 h-8 animate-spin mx-auto text-sky-400 mb-2" />
          <p className="text-xs">Fetching complaint records from SQLite backend...</p>
        </div>
      ) : filteredComplaints.length === 0 ? (
        <div className="p-12 glass-panel rounded-2xl text-center text-slate-400 border border-slate-800">
          <FileText className="w-10 h-10 mx-auto text-slate-600 mb-2" />
          <p className="text-sm font-semibold">No complaints found matching filters.</p>
        </div>
      ) : (
        <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden shadow-xl">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-900/80 text-xs font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800">
                  <th className="p-4">Complaint ID</th>
                  <th className="p-4">Category</th>
                  <th className="p-4">Language</th>
                  <th className="p-4">Priority</th>
                  <th className="p-4">Status</th>
                  <th className="p-4">Created Date</th>
                  <th className="p-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-xs text-slate-200 font-medium">
                {filteredComplaints.map((item) => (
                  <tr key={item.complaint_id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="p-4 font-mono font-bold text-sky-400">{item.complaint_id}</td>
                    <td className="p-4">{item.category}</td>
                    <td className="p-4">
                      <span
                        className={`inline-block px-2.5 py-0.5 rounded text-[11px] font-semibold border ${
                          item.language === 'Tamil'
                            ? 'bg-sky-500/10 text-sky-300 border-sky-500/30'
                            : item.language === 'Hindi'
                            ? 'bg-purple-500/10 text-purple-300 border-purple-500/30'
                            : 'bg-slate-800 text-slate-300 border-slate-700'
                        }`}
                      >
                        {item.language}
                      </span>
                    </td>
                    <td className="p-4">
                      <span
                        className={`inline-block px-2 py-0.5 rounded text-[11px] font-bold ${
                          item.priority === 'High'
                            ? 'bg-red-500/10 text-red-400 border border-red-500/30'
                            : item.priority === 'Medium'
                            ? 'bg-amber-500/10 text-amber-300 border border-amber-500/30'
                            : 'bg-slate-800 text-slate-400'
                        }`}
                      >
                        {item.priority}
                      </span>
                    </td>
                    <td className="p-4">
                      <span
                        className={`inline-block px-2.5 py-0.5 rounded-full text-[11px] font-semibold ${
                          item.status === 'Submitted'
                            ? 'bg-sky-500/10 text-sky-400 border border-sky-500/30'
                            : item.status === 'Escalated'
                            ? 'bg-amber-500/10 text-amber-400 border border-amber-500/30'
                            : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                        }`}
                      >
                        {item.status}
                      </span>
                    </td>
                    <td className="p-4 text-slate-400">
                      {new Date(item.created_at).toLocaleDateString()}
                    </td>
                    <td className="p-4 text-right">
                      <button
                        onClick={() => navigate(`/complaints/${item.complaint_id}`)}
                        className="inline-flex items-center gap-1 text-sky-400 hover:text-sky-300 font-semibold px-2.5 py-1 rounded bg-sky-500/10 hover:bg-sky-500/20 border border-sky-500/20 transition-colors"
                      >
                        <Eye className="w-3.5 h-3.5" />
                        <span>View</span>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
