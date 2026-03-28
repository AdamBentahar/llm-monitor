import streamlit as st
import pandas as pd
import sqlite3
import os

st.set_page_config(
    page_title="LLM Monitor Dashboard",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 LLM Monitoring Dashboard")
st.markdown("**EPINEON AI** — Real-time LLM tracking and recommendations")

PROFILES = {
    "coding": {"intelligence": 0.40, "speed": 0.25, "price": 0.20, "context": 0.15},
    "reasoning": {"intelligence": 0.50, "speed": 0.15, "price": 0.15, "context": 0.20},
    "rag": {"intelligence": 0.25, "speed": 0.20, "price": 0.20, "context": 0.35},
    "minimum_cost": {"intelligence": 0.20, "speed": 0.20, "price": 0.50, "context": 0.10},
    "agents": {"intelligence": 0.35, "speed": 0.30, "price": 0.20, "context": 0.15},
}

COMMERCIAL_LICENSES = {"Apache", "MIT", "Apache 2.0"}

def compute_score(model, profile):
    weights = PROFILES[profile]
    intelligence = model.get("intelligence_score_norm") or 0
    speed = model.get("speed_norm") or 0
    price = 100 - (model.get("price_norm") or 0)
    context = model.get("context_norm") or 0
    return round(
        weights["intelligence"] * intelligence +
        weights["speed"] * speed +
        weights["price"] * price +
        weights["context"] * context, 2
    )

def get_recommendations(df, profile, commercial_only=False):
    models = df.to_dict("records")
    if commercial_only:
        models = [m for m in models if m.get("license_type") in COMMERCIAL_LICENSES]
    valid = [m for m in models if any([
        m.get("intelligence_score_norm"),
        m.get("speed_norm"),
        m.get("price_norm"),
        m.get("context_norm")
    ])]
    scored = sorted(valid, key=lambda m: compute_score(m, profile), reverse=True)
    return scored[:3]

@st.cache_data
def load_data():
    csv_path = "data/models.csv"
    db_path = "llm_monitor.db"
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    elif os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        df = pd.read_sql("SELECT * FROM llm_models", conn)
        conn.close()
        return df
    return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("❌ No data found. Please run the data collection pipeline first.")
    st.stop()

# Sidebar
st.sidebar.title("⚙️ Filters")
profile = st.sidebar.selectbox("Enterprise Profile", list(PROFILES.keys()))
commercial = st.sidebar.checkbox("Commercial use only")

# Metrics row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Models", len(df))
col2.metric("Sources", df["source"].nunique() if "source" in df.columns else 0)
col3.metric("Providers", df["provider"].nunique() if "provider" in df.columns else 0)
col4.metric("Profile", profile.upper())

st.divider()

# Recommendations
st.subheader(f"🏆 Top 3 Recommendations for: {profile.upper()}")
top3 = get_recommendations(df, profile, commercial)
cols = st.columns(3)
justifications = {
    "coding": "Strong intelligence and speed make it ideal for code generation tasks.",
    "reasoning": "High reasoning capability with large context window.",
    "rag": "Large context window and good price/performance ratio for RAG pipelines.",
    "minimum_cost": "Best cost efficiency with acceptable performance.",
    "agents": "Fast response time and strong reasoning for autonomous agent tasks."
}
for i, m in enumerate(top3):
    with cols[i]:
        score = compute_score(m, profile)
        st.markdown(f"### #{i+1} {m['name']}")
        st.markdown(f"**Provider:** {m.get('provider', 'N/A')}")
        st.markdown(f"**Score:** {score}/100")
        st.markdown(f"**License:** {m.get('license_type', 'N/A')}")
        st.info(justifications[profile])

st.divider()

# Full leaderboard
st.subheader("📊 Full Model Leaderboard")
display_cols = ["name", "provider", "intelligence_score", "speed_tokens_per_sec",
                "price_input", "context_window", "license_type", "source"]
available_cols = [c for c in display_cols if c in df.columns]
st.dataframe(df[available_cols], use_container_width=True)

st.divider()

# Chart
st.subheader("📈 Intelligence Score Comparison")
chart_df = df[df["intelligence_score"].notna()][["name", "intelligence_score"]]\
    .sort_values("intelligence_score", ascending=False).head(15)
if not chart_df.empty:
    st.bar_chart(chart_df.set_index("name"))

# New models
st.subheader("🆕 Newly Detected Models (Last 24h)")
from datetime import datetime, timedelta
if "collected_at" in df.columns:
    df["collected_at"] = pd.to_datetime(df["collected_at"])
    cutoff = datetime.utcnow() - timedelta(hours=24)
    new_df = df[df["collected_at"] >= cutoff][["name", "provider", "source"]]
    if not new_df.empty:
        st.dataframe(new_df, use_container_width=True)
    else:
        st.info("No new models detected in the last 24 hours")