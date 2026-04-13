import React, { useEffect, useState, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import apiFetch from '../utils/api';
import { CheckCircle2, Clock, AlertTriangle, ArrowLeft, MessageSquare, Download, Code, Trash2 } from 'lucide-react';

export default function ProjectDetail() {
  const { id } = useParams();
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [scaffoldLoading, setScaffoldLoading] = useState(false);
  const [scaffoldResult, setScaffoldResult] = useState('');
  
  // Chat state
  const [chatOpen, setChatOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const msgEndRef = useRef(null);

  const fetchProject = () => {
    apiFetch(`/api/projects/${id}/`)
      .then(data => {
        setProject(data.project);
        setMessages(data.messages || []);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchProject();
  }, [id]);

  useEffect(() => {
    if (chatOpen && msgEndRef.current) {
      msgEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, chatOpen]);

  const handleCompleteTask = async (taskId, estimated) => {
    try {
      await apiFetch(`/api/tasks/${taskId}/complete/`, {
        method: 'POST',
        body: JSON.stringify({ actual_days: estimated })
      });
      // Refresh
      fetchProject();
    } catch (e) {
      alert("Failed to complete task: " + e.message);
    }
  };

  const handleScaffold = async (taskId) => {
    setScaffoldLoading(true);
    setScaffoldResult('Generating boilerplate and plan via AI...');
    try {
      const res = await apiFetch(`/api/tasks/${taskId}/scaffold/`, { method: 'POST' });
      setScaffoldResult(res.scaffold || "No output");
    } catch (e) {
      setScaffoldResult("Error: " + e.message);
    }
    setScaffoldLoading(false);
  };

  const sendChat = async (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;
    const msg = chatInput.trim();
    setMessages(prev => [...prev, { role: 'user', content: msg }]);
    setChatInput('');
    setChatLoading(true);

    try {
      const res = await apiFetch(`/api/projects/${id}/chat/`, {
        method: 'POST',
        body: JSON.stringify({ message: msg })
      });
      setMessages(prev => [...prev, { role: 'assistant', content: res.response }]);
    } catch (e) {
      setMessages(prev => [...prev, { role: 'assistant', content: "Error: " + e.message }]);
    }
    setChatLoading(false);
  };

  if (loading) return (
    <div className="flex h-full items-center justify-center">
      <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
    </div>
  );

  if (error || !project) return (
    <div className="glass-panel p-8 text-center text-red-400">
      <AlertTriangle className="mx-auto h-12 w-12 mb-4 opacity-50" />
      <h3 className="text-xl font-medium">Error Loading Project</h3>
      <p className="mt-2 text-red-400/70">{error}</p>
      <Link to="/dashboard" className="btn-secondary mt-4 inline-block">Back to Dashboard</Link>
    </div>
  );

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
      {/* Header */}
      <div className="flex justify-between items-start mb-8">
        <div>
          <Link to="/dashboard" className="text-sm text-indigo-400 hover:text-indigo-300 flex items-center gap-1 mb-2">
            <ArrowLeft size={16} /> Back to Projects
          </Link>
          <h1 className="text-3xl font-bold tracking-tight mb-2 max-w-2xl">{project.goal}</h1>
          <div className="flex gap-4 text-sm text-slate-400">
             <span>Started: {new Date(project.start_date || project.created_at).toLocaleDateString()}</span>
             <span>•</span>
             <span>Total Days: {project.total_days}</span>
             <span>•</span>
             <span>Status: <span className="uppercase text-white text-xs bg-white/10 px-2 py-0.5 rounded">{project.status}</span></span>
          </div>
        </div>
        <div className="flex gap-2">
          {/* Using traditional anchor for pdf export as it returns a file */}
          <a href={`/project/${project.id}/export/pdf/`} target="_blank" rel="noreferrer" className="btn-secondary flex items-center gap-2">
            <Download size={16} /> Export PDF
          </a>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main tasks list */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex justify-between items-center mb-2 border-b border-white/10 pb-2">
            <h2 className="text-xl font-semibold">Tasks ({project.tasks.length || 0})</h2>
            <div className="w-48 bg-black/30 h-2 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-emerald-500 to-teal-500 rounded-full" 
                  style={{ width: `${Math.max(project.completion_rate || 0, 2)}%` }}
                />
            </div>
          </div>
          
          {project.tasks?.map((task, idx) => (
             <div key={task.id} className="glass-panel p-5 relative overflow-hidden transition-all hover:bg-white-[0.07]">
                 <div className={`absolute top-0 bottom-0 left-0 w-1.5 ${
                    task.status === 'completed' ? 'bg-emerald-500' :
                    task.status === 'overdue' ? 'bg-red-500' : 'bg-indigo-500'
                 }`} />
                 
                 <div className="flex justify-between items-start pl-2">
                    <div>
                      <h3 className={`text-lg font-medium ${task.status === 'completed' ? 'text-slate-400 line-through' : 'text-white'}`}>
                        {task.title}
                      </h3>
                      <p className="text-sm text-slate-400 mt-1 mb-3">{task.description}</p>
                      <div className="flex gap-3 text-xs">
                        <span className="bg-black/30 px-2 py-1 rounded text-slate-300">Priority: {task.priority}</span>
                        <span className="bg-black/30 px-2 py-1 rounded text-slate-300">Est. {task.estimated_days} days</span>
                        {task.status !== 'completed' && <span className="bg-black/30 px-2 py-1 rounded text-indigo-300">Due: {task.due_date}</span>}
                      </div>
                    </div>
                    
                    <div className="flex flex-col gap-2 items-end">
                      {task.status !== 'completed' ? (
                        <>
                          <button onClick={() => handleCompleteTask(task.id, task.estimated_days)} className="btn-primary py-1.5 px-3 text-sm">
                            Mark Complete
                          </button>
                          <button onClick={() => handleScaffold(task.id)} className="text-xs text-indigo-400 hover:text-indigo-300 flex items-center gap-1">
                            <Code size={14} /> AI Scaffold
                          </button>
                        </>
                      ) : (
                         <span className="text-emerald-400 font-medium flex items-center gap-1 bg-emerald-500/10 px-3 py-1.5 rounded-lg border border-emerald-500/20"><CheckCircle2 size={16}/> Done</span>
                      )}
                    </div>
                 </div>
             </div>
          ))}
        </div>

        {/* Right Sidebar: Insights & Diagrams */}
        <div className="space-y-6">
          <div className="glass-panel p-5">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2 border-b border-white/10 pb-2">
               🧠 AI Insights
            </h2>
            <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2">
              {project.insights?.length === 0 && <p className="text-slate-400 text-sm italic">No insights generated yet.</p>}
              {project.insights?.map(insight => (
                <div key={insight.id} className="bg-black/20 rounded-lg p-3 text-sm border border-white/5">
                  <div className="font-medium text-indigo-300 mb-1 flex justify-between">
                    <span className="capitalize">{insight.agent_type} Agent</span>
                    <span className="text-[10px] text-slate-500">{new Date(insight.created_at).toLocaleDateString()}</span>
                  </div>
                  <pre className="whitespace-pre-wrap font-sans text-slate-300">{insight.message}</pre>
                </div>
              ))}
            </div>
          </div>

          <div className="glass-panel p-5">
             <h2 className="text-lg font-semibold mb-4 border-b border-white/10 pb-2">System Diagrams</h2>
             <div className="grid grid-cols-1 gap-2">
                <a href={`/project/${project.id}/usecase/`} target="_blank" className="btn-secondary text-center text-sm py-2">Use Case Diagram</a>
                <a href={`/project/${project.id}/dfd-level0/`} target="_blank" className="btn-secondary text-center text-sm py-2">DFD Level 0</a>
                <a href={`/project/${project.id}/dfd-level1/`} target="_blank" className="btn-secondary text-center text-sm py-2">DFD Level 1</a>
                <a href={`/project/${project.id}/activity/`} target="_blank" className="btn-secondary text-center text-sm py-2">Activity Diagram</a>
                <a href={`/project/${project.id}/gantt/`} target="_blank" className="bg-indigo-500/20 text-indigo-300 hover:bg-indigo-500/30 border border-indigo-500/30 text-center text-sm py-2 rounded-lg font-medium transition-colors">📅 Gantt Chart</a>
             </div>
          </div>
        </div>
      </div>

      {/* Floating Chat */}
      <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
        {chatOpen && (
          <div className="glass-panel w-80 md:w-96 h-[500px] mb-4 flex flex-col overflow-hidden shadow-2xl animate-in slide-in-from-bottom-5">
            <div className="bg-indigo-600/30 p-3 font-medium flex justify-between items-center border-b border-indigo-500/30">
              <div className="flex items-center gap-2"><MessageSquare size={18} /> Project AI Assistant</div>
              <button onClick={() => setChatOpen(false)} className="text-white/70 hover:text-white">✕</button>
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
               {messages.length === 0 && <div className="text-center text-slate-500 text-sm mt-10">Ask anything tracking to this project!</div>}
               {messages.map((msg, i) => (
                  <div key={i} className={`max-w-[85%] rounded-2xl p-3 text-sm ${msg.role === 'user' ? 'bg-indigo-500 text-white ml-auto rounded-br-none' : 'bg-white/10 text-slate-200 mr-auto rounded-bl-none'}`}>
                     {msg.content}
                  </div>
               ))}
               {chatLoading && (
                  <div className="bg-white/10 text-slate-400 mr-auto rounded-2xl rounded-bl-none p-3 text-sm italic">Thinking...</div>
               )}
               <div ref={msgEndRef} />
            </div>
            <form onSubmit={sendChat} className="p-3 border-t border-white/10 bg-black/20 flex gap-2">
               <input disabled={chatLoading} value={chatInput} onChange={e => setChatInput(e.target.value)} placeholder="Type a message..." className="flex-1 bg-black/30 border border-white/10 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
               <button disabled={chatLoading} type="submit" className="bg-indigo-500 hover:bg-indigo-600 px-3 rounded-lg flex items-center justify-center">→</button>
            </form>
          </div>
        )}
        <button onClick={() => setChatOpen(!chatOpen)} className="w-14 h-14 rounded-full bg-indigo-500 hover:bg-indigo-600 text-white shadow-[0_0_20px_rgba(99,102,241,0.5)] flex items-center justify-center transition-transform hover:scale-110">
          <MessageSquare size={24} />
        </button>
      </div>

      {/* Scaffold Modal */}
      {scaffoldResult && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
           <div className="glass-panel w-full max-w-3xl max-h-[80vh] flex flex-col shadow-2xl overflow-hidden">
              <div className="flex justify-between items-center p-4 border-b border-indigo-500/20 bg-indigo-500/10">
                 <h3 className="font-semibold flex items-center gap-2"><Code size={18}/> AI Scaffold Output</h3>
                 <button onClick={() => setScaffoldResult('')} className="text-white/50 hover:text-white text-xl">✕</button>
              </div>
              <div className="p-6 overflow-y-auto flex-1 font-mono text-sm text-slate-300 whitespace-pre-wrap leading-relaxed">
                 {scaffoldLoading ? (
                   <div className="flex flex-col items-center justify-center h-40 text-indigo-400">
                     <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-indigo-500 mb-4"></div>
                     {scaffoldResult}
                   </div>
                 ) : scaffoldResult}
              </div>
           </div>
        </div>
      )}

    </div>
  );
}
