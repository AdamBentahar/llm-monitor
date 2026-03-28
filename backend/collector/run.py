import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.database.db import init_db, SessionLocal
from backend.database.models import LLMModel
from backend.collector.huggingface import fetch_huggingface_models
from backend.collector.artificial_analysis import fetch_artificial_analysis_models
from backend.collector.normalizer import normalize_models
from datetime import datetime

def save_models(models: list):
    db = SessionLocal()
    new_count = 0
    updated_count = 0
    
    for m in models:
        existing = db.query(LLMModel).filter(LLMModel.name == m["name"]).first()
        
        if existing:
            # Update existing model
            for key, value in m.items():
                if hasattr(existing, key) and value is not None:
                    setattr(existing, key, value)
            updated_count += 1
        else:
            # Add new model
            new_model = LLMModel(**{k: v for k, v in m.items() if hasattr(LLMModel, k)})
            db.add(new_model)
            new_count += 1
    
    db.commit()
    db.close()
    print(f"✅ Saved {new_count} new models and updated {updated_count} existing models!")

def run_pipeline():
    print("🚀 Starting LLM data collection pipeline...")
    
    # Initialize database
    init_db()
    
    # Collect from all sources
    all_models = []
    
    hf_models = fetch_huggingface_models()
    all_models.extend(hf_models)
    
    aa_models = fetch_artificial_analysis_models()
    all_models.extend(aa_models)
    
    print(f"📊 Total models collected: {len(all_models)}")
    
    # Normalize
    normalized = normalize_models(all_models)
    
    # Save to database
    save_models(normalized)
    
    print("🎉 Pipeline completed successfully!")

if __name__ == "__main__":
    run_pipeline()