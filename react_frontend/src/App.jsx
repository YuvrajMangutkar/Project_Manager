import { BrowserRouter as Router, Routes, Route, Navigate, Link, useLocation } from 'react-router-dom'
import { LayoutDashboard, PlusCircle, LogOut } from 'lucide-react'
import Dashboard from './pages/Dashboard'
import CreateProject from './pages/CreateProject'
import ProjectDetail from './pages/ProjectDetail'
import Login from './pages/Login'
import Signup from './pages/Signup'

function Layout({ children }) {
  const location = useLocation();
  
  return (
    <div className="flex h-screen bg-secondary overflow-hidden text-slate-100">
      {/* Sidebar */}
      <aside className="w-64 glass-panel m-4 flex flex-col border-white/5 border-r bg-white/5 shadow-2xl backdrop-blur-xl">
        <div className="p-6 border-b border-white/5">
          <h2 className="text-xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent flex items-center gap-2">
            <span>🤖</span> AIPM
          </h2>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <Link
            to="/dashboard"
            className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
              location.pathname === '/dashboard' || location.pathname === '/'
                ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 shadow-[0_0_15px_rgba(99,102,241,0.2)]'
                : 'text-slate-400 hover:bg-white/5 hover:text-white'
            }`}
          >
            <LayoutDashboard size={20} />
            <span className="font-medium">Dashboard</span>
          </Link>
          <Link
            to="/create"
            className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
              location.pathname === '/create'
                ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                : 'text-slate-400 hover:bg-white/5 hover:text-white'
            }`}
          >
            <PlusCircle size={20} />
            <span className="font-medium">New Project</span>
          </Link>
        </nav>
        <div className="p-4 border-t border-white/5">
          <a
            href="/logout/" // traditional django logout route
            className="flex items-center gap-3 w-full px-4 py-3 text-red-400 hover:bg-red-500/10 hover:text-red-300 rounded-xl transition-all font-medium"
          >
            <LogOut size={20} />
            <span>Logout</span>
          </a>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-4 md:p-8 overflow-y-auto w-full relative">
         <div className="max-w-6xl mx-auto pb-20">
           {children}
         </div>
         {/* Background Orbs */}
         <div className="fixed top-[-10%] right-[-5%] w-[500px] h-[500px] rounded-full bg-indigo-600/20 blur-[120px] pointer-events-none -z-10" />
         <div className="fixed bottom-[-10%] left-[-10%] w-[400px] h-[400px] rounded-full bg-purple-600/20 blur-[120px] pointer-events-none -z-10" />
      </main>
    </div>
  )
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Layout><Dashboard /></Layout>} />
        <Route path="/create" element={<Layout><CreateProject /></Layout>} />
        <Route path="/project/:id" element={<Layout><ProjectDetail /></Layout>} />
        
        {/* Auth Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </Router>
  )
}

export default App
