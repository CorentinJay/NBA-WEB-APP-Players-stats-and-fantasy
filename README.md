# 🏀 NBA Stats Fantasy

Application web interactive pour l'analyse avancée de statistiques NBA destinée au fantasy basketball et aux paris sportifs.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://votre-app.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Fonctionnalités

- **📊 Dashboard Interactif** : Vue d'ensemble des statistiques NBA en temps réel
- **👤 Profils Joueurs** : Analyse détaillée avec graphiques de tendances et radar charts
- **⚖️ Comparaison** : Comparer plusieurs joueurs avec visualisations interactives
- **🏟️ Analyse d'Équipe** : Performance d'équipe et classements
- **📈 Tendances** : Évolution des performances avec moyennes mobiles
- **🎲 Prédictions ML** : Modèles pour le fantasy et les paris
- **🗂️ Explorateur de Données** : Filtres avancés et export CSV

## 🚀 Demo en Ligne

👉 **[Voir l'application](https://votre-app.streamlit.app)** 👈

## 📊 Données

- **Source** : NBA API
- **Mise à jour** : Quotidienne
- **Volume** : 160k+ observations
- **Features** : 896+ colonnes incluant :
  - Stats par joueur et par match
  - Stats d'équipe (offensive et défensive)
  - Stats adversaires
  - Métriques avancées (rotations, tendances, forme)
  - Moyennes mobiles (LAST2, LAST5, LAST10, LAST20)
  - Scores fantasy (TTFL, Sorare)

## 🛠️ Technologies

- **Frontend** : Streamlit
- **Visualisation** : Plotly
- **Data Processing** : Pandas, NumPy
- **Machine Learning** : Scikit-learn
- **Format** : Parquet (optimisé)
- **Déploiement** : Streamlit Community Cloud

## 💻 Installation Locale

```bash
# Cloner le repository
git clone https://github.com/CorentinJay/NBA_stats_fantasy.git
cd NBA_stats_fantasy

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

## 📁 Structure

```
NBA_stats_fantasy/
├── data/stats_clean.parquet    # Données (mis à jour quotidiennement)
├── app.py                      # Application Streamlit
├── .streamlit/config.toml      # Configuration
└── requirements.txt            # Dépendances
```

## 🔄 Mise à Jour des Données

Données mises à jour quotidiennement et automatiquement commitées, déclenchant le redéploiement sur Streamlit Cloud.

## 📈 Cas d'Usage

- **Fantasy Basketball** : Optimiser vos choix de joueurs
- **Paris Sportifs** : Analyser les tendances et performances
- **Analyse Statistique** : Explorer les données NBA en profondeur
- **Scouting** : Comparer les joueurs pour le recrutement

## 📝 Roadmap

- [ ] Prédictions ML en temps réel
- [ ] Comparaison de 3+ joueurs
- [ ] Export PDF des rapports
- [ ] API NBA en direct
- [ ] Mode clair/sombre
- [ ] Système de recommandation

## 👤 Auteur

**Corentin Jay**

- GitHub: [@CorentinJay](https://github.com/CorentinJay)
- Email: jay.corentin@hotmail.fr

## 📄 Licence

MIT License - Libre d'utilisation

---

⭐ Si ce projet vous plaît, donnez-lui une étoile !