import React from 'react';
import { ShieldAlert, AlertTriangle } from 'lucide-react';

export const SecurityAlert = ({ message }) => {
  if (!message) return null;

  return (
    <div className="p-4 bg-red-950/40 border border-red-500/40 rounded-xl flex items-start gap-3 text-red-200 animate-fadeIn my-3 shadow-lg shadow-red-950/20">
      <ShieldAlert className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
      <div>
        <h4 className="text-sm font-bold text-red-400">Adversarial Security Shield Activated</h4>
        <p className="text-xs text-red-200/90 mt-0.5">{message}</p>
      </div>
    </div>
  );
};
