# 🤖 AIPM — Agentic AI Project Manager

A full-stack, AI-powered project management system built with Django and deployed on Render.
It uses multi-agent reasoning to automatically break down project goals into structured tasks, track progress, evaluate risk, and generate system diagrams.

🔗 **Live Demo:** [project-manager-vu3e.onrender.com](https://project-manager-vu3e.onrender.com)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **AI Task Generation** | Groq LLM (Llama 3.1) automatically breaks a project goal into prioritized, scheduled tasks |
| 💬 **AI Chat Assistant** | Floating project-aware context AI assistant to answer questions about tasks and deadlines |
| 🪄 **AI Task Scaffolding** | One-click button to generate boilerplate code, outlines, or actionable steps for any task |
| 📄 **Executive PDF Reports** | Generates a downloadable formal status report with an AI-written executive summary |
| 📊 **Progress Tracking** | Log actual days spent per task; overdue tasks are automatically detected |
| 🔁 **Auto-Rescheduling** | When a task is delayed, all future tasks are automatically shifted |
| ⚠️ **Critic Agent** | Evaluates project health and risk level (Low / Medium / High) after each task completion |
| 🔍 **Monitor Agent** | Checks for overdue projects and generates alert insights |
| 📈 **AI Insights Panel** | Per-project feed of agent-generated insights and alerts |
| 📐 **System Diagrams** | Auto-generated Use Case, DFD Level 0, DFD Level 1, and Activity diagrams (via PlantUML) |
| ⬇️ **Diagram Download** | Download any diagram as a PNG with one click |
| 🔐 **Auth** | User signup, login, logout — each user sees only their own projects |

---

## 🛠️ Tech Stack

- **Backend:** Django 6, Python 3.12, Gunicorn
- **AI / LLM:** [Groq API](https://console.groq.com) — `llama-3.1-8b-instant` (free tier)
- **Diagrams:** [PlantUML public server](https://www.plantuml.com) (no Java required)
- **Database:** PostgreSQL (Render) / SQLite (local)
- **Deployment:** Render (Docker)
- **Static Files:** WhiteNoise

---

## 🚀 Getting Started (Local)

### 1. Clone the repository
```bash
git clone https://github.com/YuvrajMangutkar/Project_Manager.git
cd Project_Manager
```

### 2. Create a virtual environment
```bash
python -m venv env
env\Scripts\activate       # Windows
# source env/bin/activate  # Linux/Mac
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file inside the `frontend/` folder:
```env
SECRET_KEY=your-secret-key
DEBUG=True
GROQ_API_KEY=gsk_your_key_here
```
Get a free Groq API key at [console.groq.com](https://console.groq.com).

### 5. Run migrations and start the server
```bash
cd frontend
python manage.py migrate
python manage.py runserver
```

Visit `http://127.0.0.1:8000` and sign up to get started.

---

## ☁️ Deploying to Render

1. Push this repo to GitHub
2. Create a new **Web Service** on [Render](https://render.com) → select the repo → choose **Docker** runtime
3. Set these **Environment Variables** in Render:

| Variable | Value |
|---|---|
| `SECRET_KEY` | A long random string |
| `DATABASE_URL` | Auto-set if you add a Render PostgreSQL instance |
| `GROQ_API_KEY` | Your free key from [console.groq.com](https://console.groq.com) |
| `DEBUG` | `False` |

4. Click **Deploy** — Render will build the Docker image and run migrations automatically.

---

## 🏗️ Project Architecture

```
Backend First → Intelligence Upgrade → UI Enhancement
```

### Phase 1 — Core Backend
- Core models: `Project`, `Task`, `Progress`, `AIInsight`
- Planner Agent (LLM-based task generation)
- Rule-based scheduler and progress tracking

### Phase 2 — Intelligent Agents
- Critic Agent (project health + risk scoring)
- Monitor Agent (overdue detection + alerts)
- Auto-rescheduling on task delays
- Multi-agent coordination via Orchestrator

### Phase 3 — Product UI & Visualization
- Modern dark glassmorphism dashboard
- AI Insights panel per project
- Auto-generated system diagrams (UML, DFD, Activity)
- Downloadable diagram exports

---

## 📁 Repository Structure

```
aipm/
├── Dockerfile
├── Procfile
├── requirements.txt
└── frontend/
    ├── manage.py
    ├── core/               # Django settings, URLs, WSGI
    └── projects/           # Main app
        ├── models.py       # Project, Task, Progress, AIInsight
        ├── views.py        # All views
        ├── planner.py      # Groq LLM task generation
        ├── critic.py       # Critic Agent
        ├── monitor.py      # Monitor Agent
        ├── orchestrator.py # Multi-agent coordinator
        ├── plantuml_encoder.py  # Diagram URL encoder
        └── templates/      # HTML templates
```
