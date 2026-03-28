import requests

def fetch_huggingface_models():
    print("🔄 Fetching models from HuggingFace...")
    
    url = "https://huggingface.co/api/models"
    params = {
        "sort": "likes",
        "limit": 50,
        "filter": "text-generation"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    models = []
    for item in data:
        model_id = item.get("modelId", "")
        provider = model_id.split("/")[0] if "/" in model_id else "Unknown"
        license_type = item.get("cardData", {}).get("license", "Unknown")
        
        models.append({
            "name": model_id,
            "provider": provider,
            "license_type": license_type,
            "source": "HuggingFace",
            "intelligence_score": None,
            "price_input": None,
            "price_output": None,
            "speed_tokens_per_sec": None,
            "ttft_latency": None,
            "context_window": None,
        })
    
    print(f"✅ Found {len(models)} models from HuggingFace!")
    return models