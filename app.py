# =========================
# IMPORTS
# =========================



# Build the Streamlit app
import streamlit as st

# Work with API data
import pandas as pd

# Use Plotly to create interactive, fully styled charts
import plotly.express as px

import requests 

# Cache Wikipedia image lookups so Streamlit doesn't request
# the same player image every time the app reruns
@st.cache_data
def get_wikipedia_image(player_name):

    # Build the Wikipedia page-summary URL from the player's name
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + player_name.replace(" ", "_")

    # Send a request to Wikipedia
    headers = {
        "User-Agent": "NBAPlayerAnalytics/1.0"
    }

    response = requests.get(url, headers=headers)


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
# SIDEBAR
# =========================

# Keep track of which section is selected
if "page" not in st.session_state:
    st.session_state.page = "Overview"

with st.sidebar:

    st.markdown("## 🏀 NBA Analytics")
    st.caption("Player Intelligence by WillVInsights")

    st.markdown("---")

    st.markdown("### MENU")

    if st.button("🏠 Overview", use_container_width=True):
        st.session_state.page = "Overview"

    if st.button("👤 Players", use_container_width=True):
        st.session_state.page = "Players"

    if st.button("🏢 Teams", use_container_width=True):
        st.session_state.page = "Teams"

    if st.button("📊 Insights", use_container_width=True):
        st.session_state.page = "Insights"

    if st.button("ℹ️ About", use_container_width=True):
        st.session_state.page = "About"

    st.markdown("---")

    st.markdown("### FILTER PLAYERS")
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



# =========================
# KPI CARDS
# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div style="
            background:#081325;
            padding:22px;
            border-radius:18px;
            border:1px solid #1E90FF;
            box-shadow:0 0 18px rgba(30,144,255,0.35);
        ">
            <div style="color:#8FA9C9;">TOTAL PLAYERS</div>
            <div style="font-size:34px;font-weight:700;color:white;">
                {len(df):,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style="
            background:#081325;
            padding:22px;
            border-radius:18px;
            border:1px solid #22C55E;
            box-shadow:0 0 18px rgba(34,197,94,0.35);
        ">
            <div style="color:#8FA9C9;">COUNTRIES</div>
            <div style="font-size:34px;font-weight:700;color:white;">
                {df["country"].nunique()}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div style="
            background:#081325;
            padding:22px;
            border-radius:18px;
            border:1px solid #F59E0B;
            box-shadow:0 0 18px rgba(245,158,11,0.35);
        ">
            <div style="color:#8FA9C9;">NBA ANALYTICS</div>
            <div style="font-size:34px;font-weight:700;color:white;">
                V2
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div style="
            background:#081325;
            padding:22px;
            border-radius:18px;
            border:1px solid #ED174C;
            box-shadow:0 0 18px rgba(237,23,76,0.35);
        ">
            <div style="color:#8FA9C9;">STATUS</div>
            <div style="font-size:34px;font-weight:700;color:white;">
                LIVE
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# POSITION CHART
# =========================

st.subheader("Players by Position")

# Count how many players are in each position
position_counts = (
    df["position"]
    .value_counts()
    .reset_index()
)

# Give the chart columns clear names
position_counts.columns = ["Position", "Players"]

# Make basketball position abbreviations easier to understand
position_names = {
    "G": "Guard",
    "F": "Forward",
    "C": "Center",
    "G-F": "Hybrid Position",
    "F-G": "Hybrid Position",
    "F-C": "Hybrid Position",
    "C-F": "Hybrid Position"
}

position_counts["Position"] = position_counts["Position"].replace(position_names)
# Create an interactive donut chart for player positions
fig = px.pie(
    position_counts,
    names="Position",
    values="Players",
    hole=0.58,
    color="Position",
    color_discrete_sequence=[
        "#1E90FF",
        "#7C3AED",
        "#22C55E",
        "#F59E0B",
        "#ED174C",
        "#00E5FF",
        "#EC4899"
    ]
)
st.caption(
    "Hybrid Position combines players listed at multiple positions, "
    "such as Guard/Forward and Forward/Center.")
# Clean up the labels
fig.update_traces(
    textposition="inside",
    textinfo="percent+label",
    hovertemplate="<b>%{label}</b><br>Players: %{value}<br>%{percent}<extra></extra>"
)

# Match the dashboard theme
fig.update_layout(
    paper_bgcolor="#081325",
    font_color="white",
    height=420,
    margin=dict(l=20, r=20, t=20, b=20),

    legend=dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=0.85
    ),

    # Add total players in the middle of the donut
 annotations=[
    dict(
        text=f"<b>{len(df):,}</b><br><span style='font-size:14px'>Total Players</span>",
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(
            size=22,
            color="white"
        ),
        align="center"
    )
]
)
# Match the chart to the dark dashboard theme
fig.update_layout(
    paper_bgcolor="#081325",
    font_color="white",
    legend_title_text="Position",
    margin=dict(l=20, r=20, t=20, b=20)
)

# Display the Plotly chart
st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================
# PLAYER FILTER
# =========================

# Create a full player name
df["Player"] = df["first_name"] + " " + df["last_name"]

# Create the player list
player_options = df["Player"].unique()

# Set LeBron James as the default player
default_index = list(player_options).index("LeBron James")

# Create a player dropdown
selected_player = st.selectbox(
    "Select a Player",
    player_options,
    index=default_index
)

# Get the full row of data for the selected player
player = df[df["Player"] == selected_player].iloc[0]

# Get the selected player's Wikipedia image
player_image = get_wikipedia_image(selected_player)

# Show the player's image if one is found
if player_image:
    st.image(player_image, width=220)
else:
    st.info("No player image found.")

# Keep only the selected player
filtered_df = df[df["Player"] == selected_player]

# Show selected player data
st.dataframe(filtered_df)

# =========================
# FULL DATASET
# =========================

with st.expander("View Full Player Dataset"):
    st.dataframe(df, use_container_width=True)