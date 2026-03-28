PROFILES = {
    "coding": {
        "intelligence": 0.40,
        "speed": 0.25,
        "price": 0.20,
        "context": 0.15
    },
    "reasoning": {
        "intelligence": 0.50,
        "speed": 0.15,
        "price": 0.15,
        "context": 0.20
    },
    "rag": {
        "intelligence": 0.25,
        "speed": 0.20,
        "price": 0.20,
        "context": 0.35
    },
    "minimum_cost": {
        "intelligence": 0.20,
        "speed": 0.20,
        "price": 0.50,
        "context": 0.10
    },
    "agents": {
        "intelligence": 0.35,
        "speed": 0.30,
        "price": 0.20,
        "context": 0.15
    }
}

COMMERCIAL_LICENSES = {"Apache", "MIT", "Apache 2.0"}

def compute_score(model: dict, profile: str) -> float:
    weights = PROFILES.get(profile, PROFILES["reasoning"])
    
    intelligence = model.get("intelligence_score_norm") or 0
    speed = model.get("speed_norm") or 0
    price = 100 - (model.get("price_norm") or 0)  # lower price = better
    context = model.get("context_norm") or 0
    
    score = (
        weights["intelligence"] * intelligence +
        weights["speed"] * speed +
        weights["price"] * price +
        weights["context"] * context
    )
    return round(score, 2)

def get_recommendations(models: list, profile: str, commercial_only: bool = False) -> list:
    # Filter commercial licenses if needed
    if commercial_only:
        models = [m for m in models if m.get("license_type") in COMMERCIAL_LICENSES]
    
    # Filter models that have at least some data
    valid_models = [m for m in models if any([
        m.get("intelligence_score_norm"),
        m.get("speed_norm"),
        m.get("price_norm"),
        m.get("context_norm")
    ])]
    
    # Score each model
    scored = []
    for m in valid_models:
        score = compute_score(m, profile)
        scored.append({
            "model": m.get("name"),
            "provider": m.get("provider"),
            "score": score,
            "license": m.get("license_type"),
            "justification": build_justification(m, profile, score)
        })
    
    # Sort by score
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:3]

def build_justification(model: dict, profile: str, score: float) -> str:
    justifications = {
        "coding": f"Strong intelligence and speed make it ideal for code generation tasks. Score: {score}/100",
        "reasoning": f"High reasoning capability with large context window. Score: {score}/100",
        "rag": f"Large context window and good price/performance ratio for RAG pipelines. Score: {score}/100",
        "minimum_cost": f"Best cost efficiency with acceptable performance. Score: {score}/100",
        "agents": f"Fast response time and strong reasoning for autonomous agent tasks. Score: {score}/100"
    }
    return justifications.get(profile, f"Score: {score}/100")