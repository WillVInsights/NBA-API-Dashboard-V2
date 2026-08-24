# =========================
# IMPORTS
# =========================

# Call the API
import requests

# Build the Streamlit app
import streamlit as st

# Work with API data
import pandas as pd

# Pause between API requests
import time


# =========================
# PAGE TITLE
# =========================

# Show the app title
st.title("NBA API Dashboard")


# =========================
# API KEY
# =========================

# Get the API key from the private secrets file
api_key = st.secrets["BALLDONTLIE_API_KEY"]


# =========================
# API REQUEST
# =========================

# Send the API key with each request
headers = {
    "Authorization": api_key
}


@st.cache_data
def load_players():

    # Store all player records
    all_players = []

    # Start with no cursor
    cursor = None

    while True:

        # Request up to 100 players at a time
        url = "https://api.balldontlie.io/v1/players?per_page=100"

        # After the first request, use next_cursor
        if cursor is not None:
            url += f"&cursor={cursor}"

        # Make the API request
        response = requests.get(url, headers=headers)

        # Stop if the API request failed
        if response.status_code != 200:
            st.error(f"API request failed: {response.status_code}")
            break

        # Convert the response to JSON
        data = response.json()

        # Add this batch to the full player list
        all_players.extend(data["data"])

        # Get the next cursor
        cursor = data.get("meta", {}).get("next_cursor")

        # Stop when there are no more records
        if cursor is None:
            break

        # Pause 13 seconds between requests
        time.sleep(13)

    # Turn all collected player records into one dataframe
    return pd.DataFrame(all_players)


# Load saved player data from the API 

df = pd.read_csv("players.csv")
# =========================
# DATA DISPLAY
# =========================

# Show all player data 
st.dataframe(df)


# =========================
# KPI SECTION
# =========================

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Players", len(df))

with col2:
    st.metric("Countries Represented", df["country"].nunique())
# =========================
# PLAYERS BY POSITION
# =========================

st.subheader("Players by Position")

position_counts = df["position"].value_counts()

st.bar_chart(position_counts)

# =========================
# PLAYER FILTER
# =========================

# Create a full player name
df["Player"] = df["first_name"] + " " + df["last_name"]

# Create a player dropdown
selected_player = st.selectbox(
    "Select a Player",
    df["Player"].unique()
)

# Keep only the selected player
filtered_df = df[df["Player"] == selected_player]

# Show selected player data
st.dataframe(filtered_df)
