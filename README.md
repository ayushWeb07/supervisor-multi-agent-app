# 🧠 Agentic AI Application — Multi-Agent Supervisor System

A full-stack, modular, agentic AI system powered by LangGraph, LangChain, and multiple external tools. Built to handle intelligent task decomposition, multi-step reasoning, and user-friendly interaction.


### 📸 Preview

> _Embed a GIF/screenshot of the app UI (especially chat + streaming in action)_

---


## 🧩 Architecture Overview

```
                      ┌────────────┐
                      │ Supervisor │
                      └─────┬──────┘
                            ↓
        ┌──────────┬──────────────┬─────────────┬───────────────┐
        ↓          ↓              ↓             ↓               ↓
    Greeting    Enhancer       Coder     Maths Reasoner     Researcher
        │          │              │             │               │
        └──────────┴────┬─────────┴─────────────┴───────────────┘
                        ↓
                 Tool Execution Layer
            (Python REPL, Tavily, PubMed, etc.)
```

---


## 🛠️ Tech Stack

| Layer              | Tools/Frameworks                          |
| ------------------ | ----------------------------------------- |
| **Agents & Logic** | `LangChain`, `LangGraph`                  |
| **Backend**        | `FastAPI`, `Supabase` (Auth & DB)         |
| **Frontend**       | `Streamlit` with real-time chat streaming |
| **DevOps**         | `Docker`, `GitHub`, `Langsmith`           |


---


## 🧠 Agents & Tools

### 👷 Supervisor Agent

- Central brain of the system
    
- Delegates tasks to other agents
    
- Makes decisions based on outputs and history
    

### ✨ Enhancer Agent

- Improves clarity, tone, and relevance of intermediate results
    

### 💬 Greeting Agent

- Handles user onboarding and initial context setting
    

### 🧑‍💻 Coder Agent

- Writes and debugs code
    
- Uses `PythonREPL` for live execution
    

### 🧠 Maths Reasoner

- Handles symbolic & numerical problems
    
- Uses `calculator` and `PythonREPL`
    

### 🔍 Researcher

- Finds factual data and references using:
    
    - `Tavily`
        
    - `DuckDuckGo`
        
    - `Wikipedia`
        
    - `PubMed`

---


## 💡 Features

✅ Real-time **streaming chatbot interface**  
✅ **Multi-session / Multi-chat** support  
✅ **User authentication** via Supabase  
✅ Modular **agent-tool orchestration**  
✅ **LangSmith** monitoring and observability  
✅ **Dynamic memory** per chat  
✅ Fully **containerized** with Docker  
✅ Ready for **deployment** on Render etc.


---


## 🧰 Setup Instructions

### 1. Clone Repo

```
git clone https://github.com/yourusername/agentic-ai-app.git
cd agentic-ai-app
```


### 2. Environment Setup

Create `.env` file:

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
```

### 3. Run Locally


```
# Backend
uvicorn backend.fastapi_backend:app --reload

# Frontend
streamlit run .\frontend\streamlit_frontend.py
```

---


## 🧪 Tooling Integration

|Tool|Purpose|
|---|---|
|**Tavily**|Fast multi-source web search|
|**Wikipedia**|Structured encyclopedic info|
|**DuckDuckGo**|Lightweight search fallback|
|**PubMed**|Scientific paper lookup|
|**PythonREPL**|Code execution sandbox|
|**Calculator**|Basic arithmetic + formulas|

---

![LangChain](https://img.shields.io/badge/LangChain-📚-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-⚙️-purple)
![Streamlit](https://img.shields.io/badge/Streamlit-🎨-brightgreen)
![FastAPI](https://img.shields.io/badge/FastAPI-🚀-teal)
![Dockerized](https://img.shields.io/badge/Docker-Ready-blue)



## 🤝 Contributing

PRs welcome! If you're into agentic systems, AI agents, and RAG pipelines, feel free to fork, tinker, and improve.
