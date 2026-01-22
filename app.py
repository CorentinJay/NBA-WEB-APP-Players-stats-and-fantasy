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
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: {NBA_WHITE};
            color: {NBA_BLUE};
            border-radius: 4px 4px 0 0;
            padding: 10px 20px;
            font-weight: bold;
        }}
        
        .stTabs [aria-selected="true"] {{
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
        ["🏠 Accueil", "👤 Players", "🏥 Injuries", "🔮 Fantasy Predictions"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown(f"<p style='color: {NBA_WHITE}; text-align: center;'><b>Créé par Corentin Jay</b></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {NBA_WHITE}; text-align: center;'><a href='https://github.com/CorentinJay' style='color: {NBA_WHITE};'>GitHub</a></p>", unsafe_allow_html=True)

# Page d'accueil
if page == "🏠 Accueil":
    st.title("🏀 NBA Stats Fantasy")
    st.markdown("### Bienvenue sur votre dashboard NBA")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"<div style='background-color: {NBA_BLUE}; padding: 20px; border-radius: 10px; text-align: center;'>"
                   f"<h3 style='color: {NBA_WHITE};'>👤 Players</h3>"
                   f"<p style='color: {NBA_WHITE};'>Statistiques et infos des joueurs</p>"
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

# Page Players avec sous-sections
elif page == "👤 Players":
    st.title("👤 Statistiques des Joueurs")
    
    # Création des onglets pour les sous-sections
    tab1, tab2, tab3 = st.tabs(["📊 Season Stats", "📈 Career Stats", "ℹ️ Players Info"])
    
    # Onglet Season Stats
    with tab1:
        st.subheader("📊 Statistiques de la Saison")
        
        try:
            df_season = pd.read_parquet('player_season.parquet')
            st.dataframe(
                df_season,
                use_container_width=True,
                height=400,
                hide_index=True
            )
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement des stats de saison : {str(e)}")
            st.info("Vérifiez que le fichier 'player_season.parquet' est bien dans le dossier")
        
        st.markdown("---")
        st.subheader("📈 Tendances des Joueurs")
        
        try:
            df_trend = pd.read_parquet('player_trend.parquet')
            st.dataframe(
                df_trend,
                use_container_width=True,
                height=400,
                hide_index=True
            )
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement des tendances : {str(e)}")
            st.info("Vérifiez que le fichier 'player_trend.parquet' est bien dans le dossier")
        
        st.markdown("---")
        st.caption("📊 **Source des données :** NBA Official Stats API | Données mises à jour quotidiennement")
    
    # Onglet Career Stats
    with tab2:
        st.subheader("📈 Statistiques de Carrière")
        
        try:
            df_career = pd.read_parquet('player_career.parquet')
            st.dataframe(
                df_career,
                use_container_width=True,
                height=600,
                hide_index=True
            )
            
            st.markdown("---")
            st.caption("📈 **Source des données :** NBA Official Stats API | Statistiques complètes de carrière")
            
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement des stats de carrière : {str(e)}")
            st.info("Vérifiez que le fichier 'player_career.parquet' est bien dans le dossier")
    
    # Onglet Players Info
    with tab3:
        st.subheader("ℹ️ Informations des Joueurs")
        
        try:
            df_info = pd.read_parquet('player_info.parquet')
            st.dataframe(
                df_info,
                use_container_width=True,
                height=600,
                hide_index=True
            )
            
            st.markdown("---")
            st.caption("ℹ️ **Source des données :** NBA Official Stats API | Informations des joueurs")
            
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement des infos joueurs : {str(e)}")
            st.info("Vérifiez que le fichier 'player_info.parquet' est bien dans le dossier")

# Page Injuries
elif page == "🏥 Injuries":
    st.title("🏥 Injury List")
    
    try:
        df = pd.read_parquet('injury_list.parquet')
        
        st.dataframe(
            df,
            use_container_width=True,
            height=600,
            hide_index=True
        )
        
        st.markdown("---")
        st.caption("🏥 **Source des données :** ESPN injury report | Données mises à jour quotidiennement")
        
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
            height=600,
            hide_index=True
        )
        
        st.markdown("---")
        st.caption("🔮 **Source des données :** Modèle de prédiction basé sur les statistiques NBA | Prédictions générées quotidiennement")
        
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement : {str(e)}")
        st.info("Vérifiez que le fichier 'fantasy_daily_predictions.parquet' est bien dans le dossier")