# 🛠️ WORK IN PROGRESS 🛠️

# 🏀 NBA Stats Fantasy

Interactive web app to explore NBA players stats for the current season.

Provides daily predictions for fantasy basketball:
- **TrashTalk Fantasy League**: https://fantasy.trashtalk.co/
- **SORARE NBA**: https://sorare.com/fr/nba/

👉 **[View Application](https://nba-fantasy-headquarter.streamlit.app)** 👈

---

## 🛠️ DAILY PROCESS

### BACKEND (Python)

#### 1. API & Web Scraping
- NBA API extraction (box scores, players personal data, team data & season schedule)
- Injury list scraping (ESPN: https://www.espn.com/nba/injuries)
- Active rosters extraction

#### 2. Data Engineering
- Data cleaning
- Data engineering (rolling and specific stats)
- Unit tests and data drift

#### 3. Modeling
- Training on historical data, predicting on today's games for both fantasy calculation methods
- Keeping only needed data for the dashboard
- Committing to the remote repository every morning (linked to Streamlit Community Cloud)

### FRONTEND

**DAILY UPDATE FOR STATISTICS, INJURY LIST AND FANTASY PREDICTIONS**

- Interactive dashboard focused on NBA players for the current season
- Players statistics (season, career and recent trends)
- Injury list with official status (Out or Game Time Decision)
- Fantasy predictions (excluding players with 'Out' status): Trashtalk Fantasy League and SORARE NBA

---

## 📁 PROJECT STRUCTURE
```
NBA_stats_fantasy/
├── app.py                                # Dashboard code
├── fantasy_daily_predictions.parquet     # Daily fantasy predictions
├── injury_list.parquet                   # Injured players
├── stats_clean_career.parquet            # Career players stats
├── players_info.parquet                  # Players personal informations
├── stats_clean_reg_season.parquet        # Regular season players stats
├── stats_clean_post_season.parquet       # Post season players stats
├── season_schedule.parquet               # Season schedule
├── .streamlit/config.toml                # Configuration
└── requirements.txt                      # Dependencies
```

---

## 👤 Author

**Corentin Jay**

- GitHub: [@CorentinJay](https://github.com/CorentinJay)
- LinkedIn: [corentin-jay](https://www.linkedin.com/in/corentin-jay/)

---

⭐ **If you like this repo, give it a star!**