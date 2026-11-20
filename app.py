
import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="SWAG PROP FINDER",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 SWAG PROP FINDER")
st.caption("All-Sports PrizePicks Prop Scanner | Research Only")

API_URL = "https://prizepicksapi.com/api/v1/projections"
API_KEY = st.secrets["PRIZEPICKS_API_KEY"]

st.subheader("🔥 Live PrizePicks Props")

if st.button("Load All Sports Props"):
    try:
        all_props = []
        cursor = None
        pages_loaded = 0
        seen_cursors = set()

        with st.spinner("Loading available props..."):
            for page in range(5):
                params = {
                    "league":"Tennis",
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
                all_props.extend(page_props)
                pages_loaded += 1

                next_cursor = payload.get(
                    "meta", {}
                ).get("next_cursor")

                if not next_cursor:
                    break

                if next_cursor in seen_cursors:
                    st.warning("Repeated cursor detected.")
                    break

                seen_cursors.add(next_cursor)
                cursor = next_cursor

        st.success(
            f"Loaded {len(all_props)} props "
            f"from {pages_loaded} pages!"
        )

        if all_props:
            rows = []

            for prop in all_props:
                rows.append({
                    "Sport": prop.get("league", ""),
                    "Player": prop.get("player", "Unknown"),
                    "Team": prop.get("team", ""),
                    "Opponent": prop.get("opponent", ""),
                    "Stat": prop.get("stat_type", ""),
                    "Line": prop.get("line", ""),
                    "Period": prop.get("period", ""),
                    "Sides": " / ".join(
                        prop.get("sides", [])
                    )
                })

            df = pd.DataFrame(rows)

            search = st.text_input(
                "Search players, teams, sports, or stats"
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
            st.warning("No props returned by the API.")

    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
    except (ValueError, TypeError) as e:
        st.error(f"Could not process API data: {e}")
