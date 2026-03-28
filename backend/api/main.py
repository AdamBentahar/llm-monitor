import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from backend.scoring.engine import get_recommendations, PROFILES
from backend.database.db import SessionLocal
from backend.database.models import LLMModel
from datetime import datetime, timedelta

app = FastAPI(title="LLM Monitor API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "🤖 LLM Monitor API is running!"}

@app.get("/models")
def list_models():
    db = SessionLocal()
    models = db.query(LLMModel).all()
    db.close()
    return [
        {
            "id": m.id,
            "name": m.name,
            "provider": m.provider,
            "intelligence_score": m.intelligence_score,
            "price_input": m.price_input,
            "price_output": m.price_output,
            "speed_tokens_per_sec": m.speed_tokens_per_sec,
            "ttft_latency": m.ttft_latency,
            "context_window": m.context_window,
            "license_type": m.license_type,
            "source": m.source,
            "collected_at": m.collected_at,
            "intelligence_score_norm": m.intelligence_score_norm,
            "speed_norm": m.speed_norm,
            "price_norm": m.price_norm,
            "context_norm": m.context_norm,
        }
        for m in models
    ]

@app.get("/recommend")
def recommend(
    profile: str = Query(..., description="coding, reasoning, rag, agents, minimum_cost"),
    commercial: bool = Query(False)
):
    if profile not in PROFILES:
        return {"error": f"Unknown profile. Choose from: {list(PROFILES.keys())}"}
    
    db = SessionLocal()
    models = db.query(LLMModel).all()
    db.close()
    
    models_dict = [
        {
            "name": m.name,
            "provider": m.provider,
            "license_type": m.license_type,
            "intelligence_score_norm": m.intelligence_score_norm,
            "speed_norm": m.speed_norm,
            "price_norm": m.price_norm,
            "context_norm": m.context_norm,
        }
        for m in models
    ]
    
    results = get_recommendations(models_dict, profile, commercial)
    return {
        "profile": profile,
        "commercial_only": commercial,
        "recommendations": results
    }

@app.get("/new-models")
def new_models():
    db = SessionLocal()
    cutoff = datetime.utcnow() - timedelta(hours=24)
    models = db.query(LLMModel).filter(LLMModel.collected_at >= cutoff).all()
    db.close()
    return [{"name": m.name, "provider": m.provider, "source": m.source} for m in models]

@app.get("/profiles")
def list_profiles():
    return {"profiles": list(PROFILES.keys())}