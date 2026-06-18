import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import pytz
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# CONFIG & CONSTANTS
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="NBA Stats Fantasy",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

NBA_BLUE  = "#1D428A"
NBA_RED   = "#C8102E"
NBA_WHITE = "#FFFFFF"

ALL_STAR_START = date(2026, 2, 13)
ALL_STAR_END   = date(2026, 2, 18)

PAGES = ["🏠 Home", "👤 Players", "⚔️ Player VS", "🏥 Injuries", "🔮 Fantasy Predictions"]

# ─────────────────────────────────────────────
# STYLING
# ─────────────────────────────────────────────

st.markdown(f"""
<style>
    [data-testid="stSidebar"] {{ background-color: {NBA_BLUE}; }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{ color: {NBA_WHITE}; }}
    .stRadio > label {{ color: {NBA_WHITE} !important; font-weight: bold; }}
    h1 {{ color: {NBA_BLUE}; }}
    h2, h3 {{ color: {NBA_RED}; }}
    [data-testid="stMetricValue"] {{ color: {NBA_BLUE}; }}
    [data-testid="stDataFrame"] {{ border: 2px solid {NBA_BLUE}; }}
    .stButton > button {{
        background-color: {NBA_RED}; color: {NBA_WHITE};
        border: none; padding: 15px 25px;
        font-weight: bold; border-radius: 10px;
        cursor: pointer; width: 100%;
    }}
    .stButton > button:hover {{ background-color: {NBA_BLUE}; color: {NBA_WHITE}; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 8px; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {NBA_WHITE}; color: {NBA_BLUE};
        border-radius: 4px 4px 0 0; padding: 10px 20px; font-weight: bold;
    }}
    .stTabs [aria-selected="true"] {{ background-color: {NBA_BLUE}; color: {NBA_WHITE}; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────

if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown(f"<h1 style='color:{NBA_WHITE};text-align:center;'>🏀 NBA Stats</h1>", unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio(
        "Navigation",
        PAGES,
        label_visibility="collapsed",
        index=PAGES.index(st.session_state.page)
    )

    if page != st.session_state.page:
        st.session_state.page = page
        st.rerun()

    st.markdown("---")
    st.markdown(f"<p style='color:{NBA_WHITE};text-align:center;'><b>Created by Corentin Jay</b></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{NBA_WHITE};text-align:center;'><a href='https://github.com/CorentinJay' style='color:{NBA_WHITE};'>GitHub</a></p>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────

@st.cache_data(ttl=3600)
def load_parquet(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)

def load_reg_season()         : return load_parquet("stats_clean_reg_season.parquet")
def load_post_season()        : return load_parquet("stats_clean_post_season.parquet")
def load_career()             : return load_parquet("stats_clean_career.parquet")
def load_player_info()        : return load_parquet("players_info.parquet")
def load_season_schedule()    : return load_parquet("season_schedule.parquet")
def load_injury_list()        : return load_parquet("injury_list.parquet")
def load_fantasy_predictions(): return load_parquet("fantasy_daily_predictions.parquet")

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def get_paris_now() -> datetime:
    return datetime.now(pytz.timezone("Europe/Paris"))

def parse_et_to_paris(statut: str, game_date: date):
    try:
        time_str = statut.replace(" ET", "").strip().upper()
        dt_et = datetime.strptime(f"{game_date.strftime('%Y-%m-%d')} {time_str}", "%Y-%m-%d %I:%M %p")
        dt_et = pytz.timezone("US/Eastern").localize(dt_et)
        return dt_et.astimezone(pytz.timezone("Europe/Paris"))
    except Exception:
        return None

def get_today_games() -> pd.DataFrame:
    today = get_paris_now().date()
    if ALL_STAR_START <= today <= ALL_STAR_END:
        return pd.DataFrame()
    try:
        df = load_season_schedule()
        df["Date"] = pd.to_datetime(df["Date"], format="mixed", dayfirst=True)
        df["Heure_paris"] = df.apply(lambda r: parse_et_to_paris(r["Statut"], r["Date"].date()), axis=1)
        today_games = df[df["Date"].dt.date == today].copy()
        return today_games.sort_values("Heure_paris")
    except Exception as e:
        st.error(f"❌ Error loading schedule: {e}")
        return pd.DataFrame()

def format_game_display(row) -> str:
    time_str = row["Heure_paris"].strftime("%H:%M") if pd.notna(row.get("Heure_paris")) else "TBD"
    return f"{time_str} — {row['Equipe_Exterieur']} @ {row['Equipe_Domicile']} — {row['Arena']}"

def render_dataframe_with_filters(df: pd.DataFrame, key_prefix: str, height: int = 600):
    """Render a filterable dataframe — filters on PLAYER / TEAM columns."""
    filter_cols = [c for c in df.columns if "PLAYER" in c.upper() or "TEAM" in c.upper()]
    filtered = df.copy()
    if filter_cols:
        cols = st.columns(len(filter_cols))
        for idx, col in enumerate(filter_cols):
            with cols[idx]:
                choice = st.selectbox(col, ["All"] + sorted(df[col].dropna().unique().tolist()), key=f"{key_prefix}_{col}")
            if choice != "All":
                filtered = filtered[filtered[col] == choice]
    st.dataframe(filtered, use_container_width=True, height=height, hide_index=True)

def reg_season_qualify(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only players with GP >= 72 % of the season maximum GP."""
    if "GP" not in df.columns:
        return df
    threshold = df["GP"].max() * 0.72
    return df[df["GP"] >= threshold]

def render_season_leaders(df: pd.DataFrame, qualify: bool = False):
    """Display top-5 leaders for PTS / REB / AST / STL / BLK."""
    STATS = {"PTS": "🏀 Points", "REB": "🔄 Rebounds", "AST": "🎯 Assists", "STL": "🖐️ Steals", "BLK": "🚫 Blocks"}
    source = reg_season_qualify(df) if qualify else df
    player_col = next((c for c in df.columns if "PLAYER" in c.upper() and "ID" not in c.upper()), None)
    cols = st.columns(5)
    for idx, (stat, label) in enumerate(STATS.items()):
        with cols[idx]:
            st.markdown(f"**{label}**")
            if stat in source.columns and player_col:
                top5 = source.nlargest(5, stat)[[player_col, stat]].reset_index(drop=True)
                st.dataframe(top5, use_container_width=True, height=220, hide_index=True)
            else:
                st.warning(f"{stat} not found")

def create_radar_chart(
    values1, values2, categories, title,
    name1, name2, is_percentage=False
) -> go.Figure:
    if is_percentage:
        max_range = 100
        tick_vals  = [0, 20, 40, 60, 80, 100]
        suffix     = "%"
    else:
        max_val = max(values1 + values2) if (values1 + values2) else 1
        if   max_val <= 3:  max_range, tick_vals = 3.5,  [i * 0.7   for i in range(6)]
        elif max_val <= 10: max_range, tick_vals = 12,   [i * 2     for i in range(7)]
        elif max_val <= 20: max_range, tick_vals = 25,   [i * 5     for i in range(6)]
        elif max_val <= 30: max_range, tick_vals = 35,   [i * 7     for i in range(6)]
        else:               max_range = int((max_val / 10 + 1.5)) * 10; tick_vals = [i * max_range / 5 for i in range(6)]
        suffix = ""

    fig = go.Figure()
    for vals, name, color, rgba in [
        (values1, name1, NBA_BLUE, "rgba(29, 66, 138, 0.25)"),
        (values2, name2, NBA_RED,  "rgba(200, 16, 46, 0.25)"),
    ]:
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=categories, fill="toself", name=name,
            line=dict(color=color, width=3), fillcolor=rgba,
            hovertemplate="%{theta}: %{r:.1f}" + suffix + "<extra></extra>"
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, range=[0, max_range],
                tickvals=tick_vals, tickfont=dict(size=11, color="#888"),
                gridcolor="rgba(255,255,255,0.2)"
            ),
            angularaxis=dict(
                tickfont=dict(size=13, color="white", family="Arial Black"),
                gridcolor="rgba(255,255,255,0.2)"
            ),
            bgcolor="rgba(0,0,0,0)"
        ),
        title=dict(text=title, font=dict(size=16, color=NBA_BLUE, family="Arial Black"), x=0.5, xanchor="center"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.12, xanchor="center", x=0.5, font=dict(size=12)),
        height=450,
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=70, b=60, l=50, r=50)
    )
    return fig

# ─────────────────────────────────────────────
# PAGE — HOME
# ─────────────────────────────────────────────

if st.session_state.page == "🏠 Home":
    st.title("🏀 NBA Stats Fantasy")
    now = get_paris_now()
    st.markdown(f"### 📅 {now.strftime('%A, %B %d, %Y')}")
    st.markdown("---")

    # ── Today's games ──
    st.markdown("### 🏀 Today's Games")
    if ALL_STAR_START <= now.date() <= ALL_STAR_END:
        next_date = ALL_STAR_END + timedelta(days=1)
        st.info(f"🌟 ALL STAR GAME IN LOS ANGELES — Next game on {next_date.strftime('%b %d')}.")
    else:
        today_games = get_today_games()
        if not today_games.empty:
            for _, game in today_games.iterrows():
                st.markdown(
                    f"<div style='background:{NBA_WHITE};border:1px solid {NBA_BLUE};border-radius:5px;"
                    f"padding:8px;margin:5px 0;text-align:center;'>"
                    f"<p style='color:{NBA_BLUE};margin:0;font-size:14px;'>{format_game_display(game)}</p></div>",
                    unsafe_allow_html=True
                )
        else:
            st.info("No games scheduled for today.")

    st.markdown("---")

    # ── Regular season leaders ──
    st.markdown("### 📊 Regular Season Leaders")
    try:
        render_season_leaders(load_reg_season(), qualify=True)
    except Exception as e:
        st.error(f"❌ Error loading regular season stats: {e}")

    st.markdown("---")

    # ── Post season leaders ──
    st.markdown("### 🏆 Post Season Leaders")
    try:
        df_post = load_post_season()
        if df_post.empty:
            st.info("🕐 Post season has not started yet.")
        else:
            render_season_leaders(df_post, qualify=False)
    except Exception as e:
        st.error(f"❌ Error loading post season stats: {e}")

    st.markdown("---")

    # ── Navigation shortcuts ──
    st.markdown("### Navigation")
    col1, col2, col3, col4 = st.columns(4)
    shortcuts = [
        (col1, "👤 Players",            "Player statistics and info"),
        (col2, "⚔️ Player VS",          "Compare two players"),
        (col3, "🏥 Injuries",           "Injury reports"),
        (col4, "🔮 Fantasy Predictions","Fantasy predictions"),
    ]
    for col, target, subtitle in shortcuts:
        with col:
            if st.button(f"{target}\n\n{subtitle}", use_container_width=True):
                st.session_state.page = target
                st.rerun()

# ─────────────────────────────────────────────
# PAGE — PLAYERS
# ─────────────────────────────────────────────

elif st.session_state.page == "👤 Players":
    st.title("👤 Player Statistics")
    tab_season, tab_career, tab_info = st.tabs(["📊 Season Stats", "📈 Career Stats", "ℹ️ Players Info"])

    # ── Season Stats ──
    with tab_season:
        st.subheader("📊 Regular Season Statistics")
        try:
            render_dataframe_with_filters(load_reg_season(), key_prefix="reg")
        except Exception as e:
            st.error(f"❌ Error loading regular season stats: {e}")

        st.markdown("---")
        st.subheader("🏆 Post Season Statistics")
        try:
            df_post = load_post_season()
            if df_post.empty:
                st.info("🕐 Post season has not started yet.")
            else:
                render_dataframe_with_filters(df_post, key_prefix="post")
        except Exception as e:
            st.error(f"❌ Error loading post season stats: {e}")

        st.markdown("---")
        st.caption("📊 **Data Source:** NBA Official Stats API | Updated daily")

    # ── Career Stats ──
    with tab_career:
        st.subheader("📈 Career Statistics")
        try:
            render_dataframe_with_filters(load_career(), key_prefix="career")
        except Exception as e:
            st.error(f"❌ Error loading career stats: {e}")
        st.markdown("---")
        st.caption("📈 **Data Source:** NBA Official Stats API | Complete career statistics")

    # ── Players Info ──
    with tab_info:
        st.subheader("ℹ️ Player Information")
        try:
            render_dataframe_with_filters(load_player_info(), key_prefix="info")
        except Exception as e:
            st.error(f"❌ Error loading player info: {e}")
        st.markdown("---")
        st.caption("ℹ️ **Data Source:** NBA Official Stats API | Player information")

# ─────────────────────────────────────────────
# PAGE — PLAYER VS
# ─────────────────────────────────────────────

elif st.session_state.page == "⚔️ Player VS":
    st.title("⚔️ Player Comparison")

    try:
        df_season = load_reg_season()
        player_col = next((c for c in df_season.columns if "PLAYER" in c.upper() and "ID" not in c.upper()), None)

        if player_col is None:
            st.error("❌ Unable to find player names column.")
        else:
            players = sorted(df_season[player_col].dropna().unique().tolist())

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"<h3 style='color:{NBA_BLUE};text-align:center;'>Player 1</h3>", unsafe_allow_html=True)
                player1 = st.selectbox("Player 1", players, key="player1", label_visibility="collapsed")
            with col2:
                st.markdown(f"<h3 style='color:{NBA_RED};text-align:center;'>Player 2</h3>", unsafe_allow_html=True)
                player2 = st.selectbox("Player 2", players, key="player2", label_visibility="collapsed")

            p1 = df_season[df_season[player_col] == player1].iloc[0]
            p2 = df_season[df_season[player_col] == player2].iloc[0]

            def extract_stats(stat_names):
                """Extract raw counting stats (no scaling needed)."""
                vals1, vals2, labels = [], [], []
                for stat in stat_names:
                    if stat in df_season.columns:
                        vals1.append(float(p1[stat]) if pd.notna(p1[stat]) else 0.0)
                        vals2.append(float(p2[stat]) if pd.notna(p2[stat]) else 0.0)
                        labels.append(stat)
                return vals1, vals2, labels

            def extract_pct_stats(mapping):
                """Extract percentage stats, converting 0-1 values to 0-100."""
                vals1, vals2, labels = [], [], []
                for display, candidates in mapping:
                    for candidate in candidates:
                        if candidate in df_season.columns:
                            v1 = float(p1[candidate]) if pd.notna(p1[candidate]) else 0.0
                            v2 = float(p2[candidate]) if pd.notna(p2[candidate]) else 0.0
                            if 0 < v1 <= 1: v1 *= 100
                            if 0 < v2 <= 1: v2 *= 100
                            vals1.append(v1); vals2.append(v2); labels.append(display)
                            break
                return vals1, vals2, labels

            # Graph 1 — Global stats
            glb1, glb2, glb_labels = extract_stats(["PTS", "REB", "AST"])

            # Graph 2 — Offensive stats (mix of counting + percentages)
            off_pct_mapping = [
                ("FT PCT",  ["FT PCT",  "FT%"]),
                ("FG PCT",  ["FG PCT",  "FG%"]),
                ("FG3 PCT", ["FG3 PCT", "FG3%", "3P%"]),
                ("eFG PCT", ["eFG PCT", "EFG%", "eFG%"]),
            ]
            oreb1, oreb2, oreb_labels = extract_stats(["OREB"])
            pct1,  pct2,  pct_labels  = extract_pct_stats(off_pct_mapping)
            off1   = oreb1 + pct1
            off2   = oreb2 + pct2
            off_labels = oreb_labels + pct_labels

            # Graph 3 — Defensive stats
            def1, def2, def_labels = extract_stats(["DREB", "STL", "BLK", "PF"])

            st.markdown("---")
            c1, c2, c3 = st.columns(3)
            charts = [
                (c1, glb1, glb2, glb_labels, "🌐 Global Stats",      False),
                (c2, off1, off2, off_labels, "⚔️ Offensive Stats",   True),
                (c3, def1, def2, def_labels, "🛡️ Defensive Stats",   False),
            ]
            for col, v1, v2, labels, title, pct in charts:
                with col:
                    if labels:
                        st.plotly_chart(create_radar_chart(v1, v2, labels, title, player1, player2, pct), use_container_width=True)
                    else:
                        st.warning(f"{title} not available.")

            st.markdown("---")
            st.subheader("📋 Detailed Comparison")

            all_labels = glb_labels + off_labels + def_labels
            all_v1     = glb1 + off1 + def1
            all_v2     = glb2 + off2 + def2

            df_cmp = pd.DataFrame({"Stat": all_labels, player1: all_v1, player2: all_v2})
            df_cmp["Difference"] = df_cmp[player2] - df_cmp[player1]
            df_cmp["Winner"] = df_cmp.apply(
                lambda r: player1 if r[player1] > r[player2] else (player2 if r[player2] > r[player1] else "Equal"),
                axis=1
            )
            st.dataframe(df_cmp, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"❌ Error loading player data: {e}")

# ─────────────────────────────────────────────
# PAGE — INJURIES
# ─────────────────────────────────────────────

elif st.session_state.page == "🏥 Injuries":
    st.title("🏥 Injury List")
    try:
        render_dataframe_with_filters(load_injury_list(), key_prefix="injury")
        st.markdown("---")
        st.caption("🏥 **Data Source:** ESPN injury report | Updated daily")
    except Exception as e:
        st.error(f"❌ Error loading injury data: {e}")

# ─────────────────────────────────────────────
# PAGE — FANTASY PREDICTIONS
# ─────────────────────────────────────────────

elif st.session_state.page == "🔮 Fantasy Predictions":
    st.title("🔮 Fantasy Predictions")

    today_games = get_today_games()
    if not today_games.empty and "Heure_paris" in today_games.columns:
        first_time = today_games.iloc[0]["Heure_paris"]
        if pd.notna(first_time):
            st.markdown(f"### ⏰ Deadline: {first_time.strftime('%H:%M')} (first game of the day)")

    try:
        render_dataframe_with_filters(load_fantasy_predictions(), key_prefix="fantasy")
        st.markdown("---")
        st.caption("🔮 **Data Source:** Prediction model based on NBA statistics | Generated daily")
    except Exception as e:
        st.error(f"❌ Error loading fantasy predictions: {e}")