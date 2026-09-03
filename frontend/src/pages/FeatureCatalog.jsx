import React, { useState, useEffect } from 'react';
import { featureAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { Layers, ShieldCheck, ShieldAlert, Tag, Building2, AlertTriangle, Loader2 } from 'lucide-react';

export const FeatureCatalog = () => {
  const { user } = useAuth();
  const [features, setFeatures] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [permissionAlert, setPermissionAlert] = useState(null);

  useEffect(() => {
    fetchFeatures();
  }, []);

  const fetchFeatures = async () => {
    setIsLoading(true);
    try {
      const res = await featureAPI.getFeatures();
      setFeatures(res.data);
    } catch (err) {
      console.error('Failed to fetch feature catalog:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTestDirectAccess = async (featureId) => {
    setPermissionAlert(null);
    try {
      const res = await featureAPI.getFeatureById(featureId, user?.role, user?.organisation);
      setPermissionAlert({
        success: true,
        message: `✅ ACCESS GRANTED: Role '${user?.role}' is authorized for ${res.data.feature_name} (${featureId}).`,
      });
    } catch (err) {
      const reason = err.response?.data?.detail?.reason || 'Permission denied by backend RBAC policies.';
      setPermissionAlert({
        success: false,
        message: `🚫 ACCESS DENIED: ${reason}`,
      });
    }
  };

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="border-b border-slate-800 pb-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-white flex items-center gap-2.5">
            <Layers className="w-6 h-6 text-sky-400" />
            <span>Organisation Feature Catalog (F001 - F008)</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Complete metadata inventory of application features, permitted roles, and RBAC policies
          </p>
        </div>
      </div>

      {permissionAlert && (
        <div
          className={`p-4 rounded-xl text-xs font-semibold border flex items-center justify-between animate-fadeIn ${
            permissionAlert.success
              ? 'bg-emerald-950/40 border-emerald-500/40 text-emerald-300'
              : 'bg-red-950/40 border-red-500/40 text-red-300'
          }`}
        >
          <span>{permissionAlert.message}</span>
          <button onClick={() => setPermissionAlert(null)} className="text-slate-400 hover:text-white">
            Dismiss
          </button>
        </div>
      )}

      {/* Feature Grid */}
      {isLoading ? (
        <div className="p-12 text-center text-slate-400">
          <Loader2 className="w-8 h-8 animate-spin mx-auto text-sky-400 mb-2" />
          <p className="text-xs">Loading feature metadata catalog...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {features.map((feat) => {
            const isRoleAllowed =
              feat.allowed_roles.includes(user?.role || 'Citizen') || feat.allowed_roles.includes('*');

            return (
              <div
                key={feat.feature_id}
                className="glass-panel p-5 rounded-2xl border border-slate-800 hover:border-slate-700 transition-all flex flex-col justify-between space-y-4 shadow-xl"
              >
                <div className="space-y-2">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-bold text-sky-400 bg-sky-500/10 px-2.5 py-1 rounded border border-sky-500/20">
                        {feat.feature_id}
                      </span>
                      <h3 className="text-base font-bold text-white">{feat.feature_name}</h3>
                    </div>

                    <div className="flex items-center gap-1.5">
                      {feat.impact_level === 'HIGH' && (
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">
                          HIGH IMPACT
                        </span>
                      )}
                      {isRoleAllowed ? (
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                          PERMITTED
                        </span>
                      ) : (
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-red-500/20 text-red-300 border border-red-500/30">
                          RESTRICTED
                        </span>
                      )}
                    </div>
                  </div>

                  <p className="text-xs text-slate-300 leading-relaxed">{feat.description}</p>
                </div>

                <div className="space-y-2 pt-2 border-t border-slate-800/80 text-[11px] text-slate-400">
                  <div className="flex items-center gap-1.5">
                    <ShieldCheck className="w-3.5 h-3.5 text-slate-500" />
                    <span>Allowed Roles: <strong className="text-slate-300">{feat.allowed_roles}</strong></span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <Building2 className="w-3.5 h-3.5 text-slate-500" />
                    <span>Allowed Orgs: <strong className="text-slate-300">{feat.allowed_organisations}</strong></span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <Tag className="w-3.5 h-3.5 text-slate-500" />
                    <span>Task Tags: <strong className="text-slate-300">{feat.task_tags}</strong></span>
                  </div>
                </div>

                <button
                  onClick={() => handleTestDirectAccess(feat.feature_id)}
                  className="w-full py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl border border-slate-700 transition-colors"
                >
                  Test Backend Permission for Current Role ({user?.role})
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
