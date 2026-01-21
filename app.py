import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="NBA Stats Fantasy",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Couleurs NBA
NBA_BLUE = "#1D428A"
NBA_RED = "#C8102E"
NBA_WHITE = "#FFFFFF"

# CSS personnalisé avec les couleurs NBA
st.markdown(f"""
    <style>
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: {NBA_BLUE};
        }}
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
            color: {NBA_WHITE};
        }}
        
        /* Boutons de navigation */
        .stRadio > label {{
            color: {NBA_WHITE} !important;
            font-weight: bold;
        }}
        
        /* Titres */
        h1 {{
            color: {NBA_BLUE};
        }}
        
        h2, h3 {{
            color: {NBA_RED};
        }}
        
        /* Métriques */
        [data-testid="stMetricValue"] {{
            color: {NBA_BLUE};
        }}
        
        /* Tableaux */
        [data-testid="stDataFrame"] {{
            border: 2px solid {NBA_BLUE};
        }}
        
        /* Boutons */
        .stButton > button {{
            background-color: {NBA_RED};
            color: {NBA_WHITE};
        }}
        
        .stButton > button:hover {{
            background-color: {NBA_BLUE};
            color: {NBA_WHITE};
        }}
    </style>
""", unsafe_allow_html=True)

# Sidebar - Navigation
with st.sidebar:
    st.markdown(f"<h1 style='color: {NBA_WHITE}; text-align: center;'>🏀 NBA Stats</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["🏠 Accueil", "📊 Players Stats", "🏥 Injuries", "🔮 Fantasy Predictions"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown(f"<p style='color: {NBA_WHITE}; text-align: center;'><b>Créé par Corentin Jay</b></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {NBA_WHITE}; text-align: center;'><a href='https://github.com/CorentinJay' style='color: {NBA_WHITE};'>GitHub</a></p>", unsafe_allow_html=True)

# Page d'accueil
if page == "🏠 Accueil":
    st.title("🏀 NBA Stats Fantasy")
    st.markdown("### Bienvenue sur votre dashboard NBA")
    
    st.success("✅ L'application fonctionne parfaitement !")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"<div style='background-color: {NBA_BLUE}; padding: 20px; border-radius: 10px; text-align: center;'>"
                   f"<h3 style='color: {NBA_WHITE};'>📊 Players Stats</h3>"
                   f"<p style='color: {NBA_WHITE};'>Statistiques quotidiennes des joueurs</p>"
                   f"</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"<div style='background-color: {NBA_RED}; padding: 20px; border-radius: 10px; text-align: center;'>"
                   f"<h3 style='color: {NBA_WHITE};'>🏥 Injuries</h3>"
                   f"<p style='color: {NBA_WHITE};'>Liste des blessures</p>"
                   f"</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"<div style='background-color: {NBA_BLUE}; padding: 20px; border-radius: 10px; text-align: center;'>"
                   f"<h3 style='color: {NBA_WHITE};'>🔮 Predictions</h3>"
                   f"<p style='color: {NBA_WHITE};'>Prédictions Fantasy</p>"
                   f"</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("👈 Utilisez le menu de navigation à gauche pour explorer les différentes sections")

# Page Players Stats
elif page == "📊 Players Stats":
    st.title("📊 Statistiques des Joueurs")
    
    try:
        df = pd.read_parquet('stats_daily.parquet')
        
        st.dataframe(
            df,
            use_container_width=True,
            height=600
        )
        
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement : {str(e)}")
        st.info("Vérifiez que le fichier 'stats_daily.parquet' est bien dans le dossier")

# Page Injuries
elif page == "🏥 Injuries":
    st.title("🏥 Liste des Blessures")
    
    try:
        df = pd.read_parquet('injury_list.parquet')
        
        st.dataframe(
            df,
            use_container_width=True,
            height=600
        )
        
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement : {str(e)}")
        st.info("Vérifiez que le fichier 'injury_list.parquet' est bien dans le dossier")

# Page Fantasy Predictions
elif page == "🔮 Fantasy Predictions":
    st.title("🔮 Prédictions Fantasy")
    
    try:
        df = pd.read_parquet('fantasy_daily_predictions.parquet')
        
        st.dataframe(
            df,
            use_container_width=True,
            height=600
        )
        
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement : {str(e)}")
        st.info("Vérifiez que le fichier 'fantasy_daily_predictions.parquet' est bien dans le dossier")







