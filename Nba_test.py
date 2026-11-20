
import streamlit as st
from nba_api.stats.endpoints import playergamelog

st.title("NBA Stats Connection Test")

if st.button("Test NBA Stats"):
    try:
        logs = playergamelog.PlayerGameLog(
            player_id=2544,
            season="2025-26",
            timeout=15
        )

        df = logs.get_data_frames()[0]

        st.success(f"Retrieved {len(df)} games!")
        st.dataframe(df.head(10))

    except Exception as e:
        st.error(f"NBA stats connection failed: {e}")
