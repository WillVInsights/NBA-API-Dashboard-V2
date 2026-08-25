# =========================
# IMPORTS
# =========================



# Build the Streamlit app
import streamlit as st

# Work with API data
import pandas as pd

import requests 

# Get the main image from a player's Wikipedia page
def get_wikipedia_image(player_name):

    # Build the Wikipedia page-summary URL from the player's name
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + player_name.replace(" ", "_")

    # Send a request to Wikipedia
    headers = {
        "User-Agent": "NBAPlayerAnalytics/1.0"
    }

    response = requests.get(url, headers=headers)

    # Temporary test output
    print("Wikipedia URL:", url)
    print("Status code:", response.status_code)

    # Continue only if Wikipedia returned the page successfully
    if response.status_code == 200:
        data = response.json()

        # Return the main image URL if the page has one
        if "originalimage" in data:
            return data["originalimage"]["source"]

    # Return nothing if no image is found
    return None
    
st.set_page_config(
    page_title="NBA Player Analytics",
    page_icon="🏀",
    layout="wide"
)
# =========================
# PAGE TITLE
# =========================

# Show the app title
st.title("🏀 NBA Player Analytics")


# Load saved player data  

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
player = df[df["Player"] == selected_player].iloc[0]

player_image = get_wikipedia_image(selected_player)

if player_image:
    st.image(player_image, width=220)
else:
    st.info("No player image found.")


# Keep only the selected player
filtered_df = df[df["Player"] == selected_player]

# Show selected player data
st.dataframe(filtered_df)
