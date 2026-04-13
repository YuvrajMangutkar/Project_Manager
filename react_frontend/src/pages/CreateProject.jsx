import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiFetch from '../utils/api';
import { Rocket, Target, CalendarDays, AlertTriangle } from 'lucide-react';

export default function CreateProject() {
  const [goal, setGoal] = useState('');
  const [days, setDays] = useState(7);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Assuming our Django view processes form-encoded goals and days nicely, or json
      await apiFetch('/api/projects/create/', {
        method: 'POST',
        body: JSON.stringify({ goal, total_days: days })
      });
      // Redirect to dashboard on success
      navigate('/dashboard');
    } catch (err) {
      setError(err.message || 'Failed to create project');
      setLoading(false);
    }
  };

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-700 max-w-3xl mx-auto">
      <div className="text-center mb-10">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-indigo-500/20 text-indigo-400 mb-4 shadow-[0_0_30px_rgba(99,102,241,0.3)]">
          <Rocket size={32} />
        </div>
        <h1 className="text-4xl font-bold tracking-tight mb-2">Initialize New Project</h1>
        <p className="text-slate-400">Describe your goal, and our multi-agent system will break it down into a scheduled task list automatically.</p>
      </div>

      <div className="glass-panel p-8 relative overflow-hidden">
        {/* Glow effect */}
        <div className="absolute -top-32 -right-32 w-64 h-64 bg-indigo-500/20 rounded-full blur-[80px]" />
        
        {error && (
          <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl mb-6 flex items-center gap-3">
            <AlertTriangle size={20} />
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6 relative z-10">
          <div>
            <label className="flex items-center gap-2 text-sm font-medium text-slate-300 mb-2">
              <Target size={16} /> 
              Project Goal / Objective
            </label>
            <textarea
              required
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              placeholder="e.g. Build a comprehensive dashboard for tracking healthcare metrics..."
              className="w-full bg-black/20 border border-white/10 rounded-xl p-4 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent min-h-[120px] transition-all"
            />
          </div>

          <div>
            <label className="flex items-center gap-2 text-sm font-medium text-slate-300 mb-2">
              <CalendarDays size={16} />
              Estimated Total Timeline (Days)
            </label>
            <div className="flex items-center gap-4">
              <input
                type="range"
                min="1"
                max="90"
                value={days}
                onChange={(e) => setDays(Number(e.target.value))}
                className="w-full accent-indigo-500"
              />
              <div className="bg-black/20 border border-white/10 rounded-lg px-4 py-2 font-mono text-xl text-indigo-300 w-24 text-center">
                {days}
              </div>
            </div>
          </div>

          <div className="pt-6 border-t border-white/5">
            <button
              type="submit"
              disabled={loading}
              className={`w-full py-4 rounded-xl font-bold text-lg shadow-[0_0_20px_rgba(99,102,241,0.4)] transition-all flex items-center justify-center gap-2 ${
                loading ? 'bg-indigo-500/50 cursor-not-allowed' : 'bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-400 hover:to-purple-400'
              }`}
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></div>
                  Generating AI Plan...
                </>
              ) : (
                <>
                  <Rocket size={20} />
                  Launch Project
                </>
              )}
            </button>
            <p className="text-center text-xs text-slate-500 mt-4">
              Our Planner Agent will process your goal using LLM and create an optimal execution strategy.
            </p>
          </div>
        </form>
      </div>
    </div>
  );
}
