import React, { useState } from 'react';
import { Sparkles, HelpCircle, ArrowRight, ShieldCheck, AlertCircle, ThumbsUp, ThumbsDown, Check } from 'lucide-react';
import { recommendationAPI } from '../services/api';

export const RecommendationCard = ({ recommendation, onExplain, onExecute }) => {
  const [feedbackSent, setFeedbackSent] = useState(null);

  if (!recommendation) return null;

  const scorePct = Math.min(Math.max(recommendation.score, 0), 100);

  const handleRating = async (isHelpful) => {
    try {
      await recommendationAPI.submitFeedback({
        recommendation_id: recommendation.id || 1,
        anonymous_user_id: 'USER_001',
        is_helpful: isHelpful,
        feedback_text: isHelpful ? 'User found recommendation relevant' : 'User rated recommendation unhelpful'
      });
      setFeedbackSent(isHelpful);
    } catch (err) {
      console.error('Feedback submission error:', err);
    }
  };

  return (
    <div className="p-5 rounded-2xl bg-gradient-to-br from-slate-800/80 to-slate-900 border border-sky-500/30 shadow-xl space-y-4">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/20">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[11px] font-bold text-sky-400 uppercase tracking-wider">Top Recommendation</span>
            <h3 className="text-lg font-bold text-white">{recommendation.feature_name}</h3>
          </div>
        </div>

        <div className="text-right">
          <span className="text-xl font-extrabold text-emerald-400">{recommendation.score}</span>
          <span className="text-xs text-slate-400">/100</span>
          {recommendation.hybrid_similarity_score > 0 && (
            <p className="text-[10px] text-sky-400 font-mono">TF-IDF: {(recommendation.hybrid_similarity_score * 100).toFixed(0)}%</p>
          )}
        </div>
      </div>

      <p className="text-xs text-slate-300 leading-relaxed">{recommendation.description}</p>

      {/* Score Progress Bar */}
      <div>
        <div className="flex justify-between text-[11px] font-medium text-slate-400 mb-1">
          <span>Explainable Match Score</span>
          <span>{recommendation.score}% Match</span>
        </div>
        <div className="w-full bg-slate-900 h-2 rounded-full overflow-hidden border border-slate-700/50">
          <div
            className="bg-gradient-to-r from-sky-500 to-emerald-400 h-full transition-all duration-500"
            style={{ width: `${scorePct}%` }}
          ></div>
        </div>
      </div>

      {/* Status Badges */}
      <div className="flex flex-wrap items-center justify-between gap-2 pt-1">
        <div className="flex flex-wrap items-center gap-2">
          {recommendation.allowed ? (
            <span className="inline-flex items-center gap-1 text-[11px] px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">
              <ShieldCheck className="w-3.5 h-3.5" />
              Permission Granted
            </span>
          ) : (
            <span className="inline-flex items-center gap-1 text-[11px] px-2.5 py-0.5 rounded-full bg-red-500/10 text-red-300 border border-red-500/30">
              <AlertCircle className="w-3.5 h-3.5" />
              Role Access Restricted
            </span>
          )}

          {recommendation.requires_confirmation && (
            <span className="inline-flex items-center gap-1 text-[11px] px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-300 border border-amber-500/30">
              ⚠️ High-Impact Confirmation Required
            </span>
          )}
        </div>

        {/* Feedback Rating Buttons */}
        <div className="flex items-center gap-1.5 bg-slate-900/60 p-1 rounded-lg border border-slate-800 text-xs">
          <span className="text-[10px] text-slate-500 font-semibold px-1">Helpful?</span>
          {feedbackSent !== null ? (
            <span className="text-[10px] text-emerald-400 font-semibold flex items-center gap-1 px-1">
              <Check className="w-3 h-3" /> Recorded
            </span>
          ) : (
            <>
              <button
                onClick={() => handleRating(true)}
                className="p-1 rounded hover:bg-slate-800 text-slate-400 hover:text-emerald-400 transition-colors"
                title="Helpful"
              >
                <ThumbsUp className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => handleRating(false)}
                className="p-1 rounded hover:bg-slate-800 text-slate-400 hover:text-red-400 transition-colors"
                title="Not Helpful"
              >
                <ThumbsDown className="w-3.5 h-3.5" />
              </button>
            </>
          )}
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center justify-between pt-2 border-t border-slate-800">
        <button
          onClick={onExplain}
          className="inline-flex items-center gap-1.5 text-xs text-sky-400 hover:text-sky-300 font-semibold px-2 py-1 rounded hover:bg-sky-500/10 transition-colors"
        >
          <HelpCircle className="w-4 h-4" />
          <span>Why this recommendation?</span>
        </button>

        <button
          onClick={onExecute}
          className="inline-flex items-center gap-1.5 px-4 py-2 bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold rounded-lg text-xs transition-colors shadow-lg shadow-sky-500/20"
        >
          <span>Open Feature</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};
