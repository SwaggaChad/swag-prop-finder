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
        response = requests.get(
            API_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            params={
                "league": "NBA",
                "view": "compact",
                "limit": 5
            },
            timeout=20
        )
        response.raise_for_status()
        st.success("API request successful!")
        st.json(response.json())
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")

