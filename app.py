import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="NBA Stats Fantasy",
    page_icon="🏀",
    layout="wide"
)

# Titre
st.title("🏀 NBA Stats Fantasy")
st.markdown("### Application de test")

# Message de bienvenue
st.success("✅ L'application fonctionne parfaitement !")

# Essayer de charger les données
try:
    df = pd.read_parquet('stats_clean.parquet')
    
    st.subheader("📊 Données chargées avec succès")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Nombre de lignes", f"{len(df):,}")
    
    with col2:
        st.metric("Nombre de colonnes", len(df.columns))
    
    with col3:
        st.metric("Joueurs uniques", df['PLAYER_NAME'].nunique() if 'PLAYER_NAME' in df.columns else "N/A")
    
    # Afficher un aperçu
    st.subheader("📋 Aperçu des données")
    st.dataframe(df.head(10))
    
except Exception as e:
    st.error(f"❌ Erreur lors du chargement : {str(e)}")
    st.info("Vérifiez que le fichier 'stats_clean.parquet' est bien dans le dossier")

# Footer
st.markdown("---")
st.markdown("**Créé par Corentin Jay** | [GitHub](https://github.com/CorentinJay)")