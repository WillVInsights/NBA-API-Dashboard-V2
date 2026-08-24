# =========================
# IMPORTS
# =========================



# Build the Streamlit app
import streamlit as st

# Work with API data
import pandas as pd



# =========================
# PAGE TITLE
# =========================

# Show the app title
st.title("NBA API Dashboard")


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

# Keep only the selected player
filtered_df = df[df["Player"] == selected_player]

# Show selected player data
st.dataframe(filtered_df)
