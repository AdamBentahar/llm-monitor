def normalize(value, min_val, max_val):
    """Normalize a value to 0-100 scale"""
    if value is None:
        return None
    if max_val == min_val:
        return 50
    return round((value - min_val) / (max_val - min_val) * 100, 2)

def normalize_models(models: list) -> list:
    print("🔄 Normalizing models...")
    
    # Get all values for each metric (ignoring None)
    scores = [m["intelligence_score"] for m in models if m.get("intelligence_score")]
    speeds = [m["speed_tokens_per_sec"] for m in models if m.get("speed_tokens_per_sec")]
    prices = [m["price_input"] for m in models if m.get("price_input")]
    contexts = [m["context_window"] for m in models if m.get("context_window")]
    
    for m in models:
        # Normalize intelligence score
        if m.get("intelligence_score") and scores:
            m["intelligence_score_norm"] = normalize(
                m["intelligence_score"], min(scores), max(scores)
            )
        else:
            m["intelligence_score_norm"] = None
            
        # Normalize speed
        if m.get("speed_tokens_per_sec") and speeds:
            m["speed_norm"] = normalize(
                m["speed_tokens_per_sec"], min(speeds), max(speeds)
            )
        else:
            m["speed_norm"] = None
            
        # Normalize price (lower is better)
        if m.get("price_input") and prices:
            m["price_norm"] = normalize(
                m["price_input"], min(prices), max(prices)
            )
        else:
            m["price_norm"] = None
            
        # Normalize context window
        if m.get("context_window") and contexts:
            m["context_norm"] = normalize(
                m["context_window"], min(contexts), max(contexts)
            )
        else:
            m["context_norm"] = None
    
    print(f"✅ Normalized {len(models)} models!")
    return models