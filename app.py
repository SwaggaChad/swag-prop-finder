
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time
st.set_page_config(
    page_title="SWAG PROP FINDER",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 SWAG PROP FINDER")
st.caption("Multi-Sport Prop Scanner | Research Only")

API_URL = "https://prizepicksapi.com/api/v1/projections"
API_KEY = st.secrets["PRIZEPICKS_API_KEY"]

LEAGUES = [
    "NBA",
    "NFL",
    "MLB",
    "NHL",
    "Tennis",
    "Soccer",
    "WNBA",
    "NCAAB",
    "NCAAF",
    "PGA",
    "MMA",
    "CS2",
    "LoL"
]

st.subheader("🔥 Live PrizePicks Props")

selected_leagues = st.multiselect(
    "Choose sports to scan",
    LEAGUES,
    default=LEAGUES
)

if st.button("Load Selected Sports Props"):
    all_props = []
    scan_results = []
    errors = []

    with st.spinner("Scanning sports and loading props..."):
        for league in selected_leagues:
            cursor = None
            seen_cursors = set()
            league_count = 0

            try:
                for page in range(5):
                    params = {
                        "league": league,
                        "view": "compact",
                        "limit": 100
                    }

                    if cursor:
                        params["cursor"] = cursor

                    response = requests.get(
                        API_URL,
                        headers={
                            "Authorization": f"Bearer {API_KEY}"
                        },
                        params=params,
                        timeout=20
                    )
                    response.raise_for_status()

                    payload = response.json()
                    page_props = payload.get("data", [])

                    for prop in page_props:
                        prop["_scanned_league"] = league

                    all_props.extend(page_props)
                    league_count += len(page_props)

                    next_cursor = payload.get(
                        "meta", {}
                    ).get("next_cursor")

                    if not next_cursor:
                        break

                    if next_cursor in seen_cursors:
                        break

                    seen_cursors.add(next_cursor)
                    cursor = next_cursor

                scan_results.append({
                    "Sport": league,
                    "Props": league_count
                })

            except (requests.RequestException, ValueError, TypeError) as e:
                errors.append(f"{league}: {e}")

    st.success(
        f"Loaded {len(all_props)} props "
        f"across {len(scan_results)} scanned leagues!"
    )

    if scan_results:
        st.subheader("📊 Props by Sport")
        st.dataframe(
            pd.DataFrame(scan_results),
            hide_index=True,
            use_container_width=True
        )

    if errors:
        st.warning("Some leagues could not be loaded:")
        for error in errors:
            st.write(error)

    if all_props:
        rows = []

        for prop in all_props:
            sides = prop.get("sides", [])
            if not isinstance(sides, list):
                sides = []

            rows.append({
                "Sport": prop.get(
                    "league",
                    prop.get("_scanned_league", "")
                ),
                "Player": prop.get("player", "Unknown"),
                "Team": prop.get("team", ""),
                "Opponent": prop.get("opponent", ""),
                "Stat": prop.get(
                    "stat_type",
                    prop.get("stat", "")
                ),
                "Line": prop.get("line", ""),
                "Period": prop.get("period", ""),
                "Sides": " / ".join(map(str, sides))
            })

        df = pd.DataFrame(rows)

        st.subheader("🏆 All Sports Prop Board")

        search = st.text_input(
            "Search player, team, sport, or stat"
        )

        if search:
            mask = df.astype(str).apply(
                lambda col: col.str.contains(
                    search,
                    case=False,
                    regex=False
                )
            ).any(axis=1)

            df = df[mask]

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.warning("No props were returned.")
