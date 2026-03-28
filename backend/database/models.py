from sqlalchemy import Column, String, Float, Integer, DateTime, create_engine
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class LLMModel(Base):
    __tablename__ = "llm_models"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    provider = Column(String)
    intelligence_score = Column(Float)
    intelligence_score_norm = Column(Float)
    price_input = Column(Float)
    price_output = Column(Float)
    price_norm = Column(Float)
    speed_tokens_per_sec = Column(Float)
    speed_norm = Column(Float)
    ttft_latency = Column(Float)
    context_window = Column(Integer)
    context_norm = Column(Float)
    license_type = Column(String)
    source = Column(String)
    collected_at = Column(DateTime, default=datetime.utcnow)