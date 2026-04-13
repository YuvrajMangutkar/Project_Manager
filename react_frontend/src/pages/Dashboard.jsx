import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import apiFetch from '../utils/api';
import { CheckCircle2, AlertCircle, Clock, CalendarDays, Rocket } from 'lucide-react';

export default function Dashboard() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    apiFetch('/api/projects/')
      .then(data => {
        setProjects(data.projects || []);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return (
    <div className="flex h-full items-center justify-center">
      <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
    </div>
  );

  if (error) return (
    <div className="glass-panel p-8 text-center text-red-400">
      <AlertCircle className="mx-auto h-12 w-12 mb-4 opacity-50" />
      <h3 className="text-xl font-medium">Error Loading Projects</h3>
      <p className="mt-2 text-red-400/70">{error}</p>
    </div>
  );

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex justify-between items-end mb-8">
        <div>
          <h1 className="text-4xl font-bold tracking-tight mb-2">My Projects</h1>
          <p className="text-slate-400">Manage your agent-assisted projects.</p>
        </div>
        <Link to="/create" className="btn-primary shadow-indigo-500/50 flex items-center gap-2">
          <Rocket size={18} />
          Create New Project
        </Link>
      </div>

      {projects.length === 0 ? (
        <div className="glass-panel border-dashed border-2 border-white/10 p-16 text-center text-slate-400 flex flex-col items-center">
          <div className="bg-white/5 p-6 rounded-full mb-6">
            <svg className="w-16 h-16 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
          <h3 className="text-2xl font-medium text-white mb-2">No projects yet</h3>
          <p className="mb-6 max-w-sm">Get started by giving our AI Planner a goal. It will automatically break it down into actionable tasks.</p>
          <Link to="/create" className="btn-primary">Create Your First Project</Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map(project => (
            <Link key={project.id} to={`/project/${project.id}`} className="group">
              <div className="glass-panel p-6 h-full transition-all duration-300 hover:shadow-2xl hover:-translate-y-1 hover:border-indigo-500/30 flex flex-col relative overflow-hidden">
                {/* Decorative top border based on status */}
                <div className={`absolute top-0 left-0 right-0 h-1 ${
                  project.status === 'completed' ? 'bg-emerald-500' :
                  project.status === 'overdue' ? 'bg-red-500' : 'bg-indigo-500'
                }`} />
                
                <h3 className="text-xl font-semibold mb-3 pr-8 line-clamp-2">{project.goal}</h3>
                
                <div className="flex flex-wrap gap-2 mb-6 text-sm">
                  {project.status === 'completed' && <span className="bg-emerald-500/20 text-emerald-400 px-3 py-1 rounded-full flex items-center gap-1 border border-emerald-500/20"><CheckCircle2 size={14}/> Completed</span>}
                  {project.status === 'overdue' && <span className="bg-red-500/20 text-red-400 px-3 py-1 rounded-full flex items-center gap-1 border border-red-500/20"><AlertCircle size={14}/> Overdue</span>}
                  {project.status === 'in_progress' && <span className="bg-indigo-500/20 text-indigo-400 px-3 py-1 rounded-full flex items-center gap-1 border border-indigo-500/20"><Clock size={14}/> In Progress</span>}
                  
                  <span className="bg-white/5 text-slate-300 px-3 py-1 rounded-full flex items-center gap-1 border border-white/10">
                    <CalendarDays size={14}/> {project.total_days} Days Target
                  </span>
                </div>

                <div className="mt-auto pt-4 border-t border-white/5">
                  <div className="flex justify-between text-sm mb-2 text-slate-400">
                    <span>Started: {new Date(project.start_date || project.created_at).toLocaleDateString()}</span>
                    <span>{Math.round(project.completion_rate)}%</span>
                  </div>
                  <div className="w-full bg-black/30 h-2 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full transition-all duration-1000 ease-out" 
                      style={{ width: `${Math.max(project.completion_rate || 0, 2)}%` }}
                    />
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
