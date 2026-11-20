
import streamlit as st

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
