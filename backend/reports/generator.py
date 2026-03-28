import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from datetime import datetime
from backend.database.db import SessionLocal
from backend.database.models import LLMModel
from backend.scoring.engine import get_recommendations, PROFILES

def generate_report():
    print("📝 Generating digest report...")
    
    db = SessionLocal()
    models = db.query(LLMModel).all()
    db.close()
    
    models_dict = [
        {
            "name": m.name,
            "provider": m.provider,
            "license_type": m.license_type,
            "intelligence_score": m.intelligence_score,
            "price_input": m.price_input,
            "speed_tokens_per_sec": m.speed_tokens_per_sec,
            "context_window": m.context_window,
            "intelligence_score_norm": m.intelligence_score_norm,
            "speed_norm": m.speed_norm,
            "price_norm": m.price_norm,
            "context_norm": m.context_norm,
        }
        for m in models
    ]
    
    lines = []
    lines.append("# 📊 LLM Monitor Digest Report")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Total Models Tracked:** {len(models_dict)}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    for profile in PROFILES:
        lines.append(f"## 🏷️ Profile: {profile.upper()}")
        top = get_recommendations(models_dict, profile)
        
        if not top:
            lines.append("No recommendations available.")
            continue
            
        for i, r in enumerate(top, 1):
            lines.append(f"**#{i} {r['model']}** ({r['provider']})")
            lines.append(f"- Score: {r['score']}/100")
            lines.append(f"- License: {r['license']}")
            lines.append(f"- {r['justification']}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    lines.append("## 📌 Summary")
    lines.append(f"- Total models monitored: {len(models_dict)}")
    lines.append(f"- Report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"- Profiles analyzed: {', '.join(PROFILES.keys())}")
    
    report = "\n".join(lines)
    
    os.makedirs("reports", exist_ok=True)
    with open("reports/digest.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("✅ Report generated at reports/digest.md")
    return report

if __name__ == "__main__":
    generate_report()