import requests
import streamlit as st
API_KEY = st.secrets["PRIZEPICKS_API_KEY"]
API_URL = "https://prizepicksapi.com/api/v1/projections"
st.set_page_config(
    page_title="SWAG PROP FINDER",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 SWAG PROP FINDER")
st.caption("PrizePicks + Novig Betting Analysis")

st.success("Dashboard setup successful!")

sports = [
    "NBA", "NFL", "NHL", "MLB",
    "CFB", "Soccer", "Tennis"
]

sport = st.selectbox("Choose your sport", sports)

st.subheader("Today's Top 6 Props")
st.info("Live props will appear after we connect the API.")

st.subheader("Line Movement Alerts")
st.info("Alerts will appear after we set up monitoring.")

st.caption("Research only. No guaranteed picks.")


st.subheader("🏀 Live PrizePicks Props")

if st.button("Load Live NBA Props"):
    try:
        all_props = []
        cursor = None
        pages_loaded = 0
        for page in range (5):
            params = {
            "view": "compact",
            "limit": 100
        }

        if cursor:
           params["cursor"] = cursor
        response = requests.get(
                API_URL,
                headers={"Authorization": f"Bearer {API_KEY}"},
                params=params,
                timeout=20
        )
        response.raise_for_status()
        

        payload = response.json()
        all_props.extend(payload.get("data", []))
        pages_loaded += 1
        cursor = payload.get("meta", {}).get("next_cursor")
        if not cursor:
           break
        
        
        st.success(f"Loaded {len(all_props)} props from {pages_loaded} pages!")
        props = all_props

        if props:
            rows = []
            for prop in props:
                rows.append({
                     "Player": prop.get("player", "Unknown"),
                     "Team": prop.get("team", ""),
                     "Opponent": prop.get("opponent", ""),
                     "Stat": prop.get("stat", ""),
                     "Line": prop.get("line", ""),
                     "Period": prop.get("period", ""),
                     "Sides": " / ".join(prop.get("sides", []))
                    })
            st.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            st.warning("No props returned for this request.")
        
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")

