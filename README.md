# 🤖 LLM Monitoring System — EPINEON AI Challenge 2026

## 📌 Overview
An automated system for collecting, normalizing, scoring, and recommending LLMs for enterprise use cases.

## 🏗️ Architecture
- **Module 1** — Data collection from HuggingFace & Artificial Analysis (65+ models)
- **Module 2** — Composite scoring engine with 5 enterprise profiles + REST API
- **Module 3** — Streamlit dashboard + auto-generated digest report
- **Bonus** — Automated daily scheduler (APScheduler)

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/AdamBentahar/llm-monitor.git
cd llm-monitor
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run data collection
```bash
python backend/collector/run.py
```

### 5. Start the API
```bash
uvicorn backend.api.main:app --reload
```

### 6. Start the dashboard
```bash
streamlit run frontend/dashboard.py
```

### 7. Generate report
```bash
python backend/reports/generator.py
```

### 8. Run automated scheduler
```bash
python scheduler.py
```

## 🌐 API Endpoints
- `GET /models` — List all models
- `GET /recommend?profile=coding&commercial=true` — Get top 3 recommendations
- `GET /new-models` — Get newly detected models
- `GET /profiles` — List all profiles

## 🏷️ Enterprise Profiles
| Profile | Focus |
|---|---|
| coding | Intelligence + Speed |
| reasoning | Intelligence + Context |
| rag | Context Window + Price |
| agents | Speed + Intelligence |
| minimum_cost | Price efficiency |

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, SQLAlchemy, SQLite
- **Frontend:** Streamlit
- **Scheduler:** APScheduler
- **Data Sources:** HuggingFace API, Artificial Analysis

## 👤 Author
Adam Bentahar — ESITH 2025/2026