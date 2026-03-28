import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="LLM Monitor Dashboard",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 LLM Monitoring Dashboard")
st.markdown("**EPINEON AI** — Real-time LLM tracking and recommendations")

API_URL = "http://127.0.0.1:8000"

# Sidebar
st.sidebar.title("⚙️ Filters")
profile = st.sidebar.selectbox(
    "Enterprise Profile",
    ["coding", "reasoning", "rag", "agents", "minimum_cost"]
)
commercial = st.sidebar.checkbox("Commercial use only")

# Load models
try:
    response = requests.get(f"{API_URL}/models")
    models = response.json()
    df = pd.DataFrame(models)
except:
    st.error("❌ API is not running! Please start the API first.")
    st.stop()

# Metrics row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Models", len(df))
col2.metric("Sources", df["source"].nunique() if "source" in df.columns else 0)
col3.metric("Providers", df["provider"].nunique() if "provider" in df.columns else 0)
col4.metric("Profile", profile.upper())

st.divider()

# Recommendations
st.subheader(f"🏆 Top 3 Recommendations for: {profile.upper()}")
try:
    reco = requests.get(f"{API_URL}/recommend?profile={profile}&commercial={commercial}").json()
    cols = st.columns(3)
    for i, r in enumerate(reco["recommendations"]):
        with cols[i]:
            st.markdown(f"### #{i+1} {r['model']}")
            st.markdown(f"**Provider:** {r['provider']}")
            st.markdown(f"**Score:** {r['score']}/100")
            st.markdown(f"**License:** {r['license']}")
            st.info(r['justification'])
except:
    st.error("Could not load recommendations")

st.divider()

# Full leaderboard
st.subheader("📊 Full Model Leaderboard")
display_cols = ["name", "provider", "intelligence_score", "speed_tokens_per_sec", 
                "price_input", "context_window", "license_type", "source"]
available_cols = [c for c in display_cols if c in df.columns]
st.dataframe(df[available_cols], use_container_width=True)

st.divider()

# Charts
st.subheader("📈 Intelligence Score Comparison")
chart_df = df[df["intelligence_score"].notna()][["name", "intelligence_score"]].sort_values(
    "intelligence_score", ascending=False).head(15)
st.bar_chart(chart_df.set_index("name"))

# New models
st.subheader("🆕 Newly Detected Models (Last 24h)")
try:
    new = requests.get(f"{API_URL}/new-models").json()
    if new:
        st.dataframe(pd.DataFrame(new), use_container_width=True)
    else:
        st.info("No new models detected in the last 24 hours")
except:
    st.error("Could not load new models")