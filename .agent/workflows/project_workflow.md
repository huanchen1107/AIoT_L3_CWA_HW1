---
description: Taiwan Weather Forecast project - full development workflow
---

# Taiwan Weather Forecast — Project Workflow

## 1. Setup Environment
Install all required Python packages.

```bash
pip install requests pandas streamlit folium streamlit-folium
```

## 2. Fetch Weather Data from CWA API
Run the data fetch script to pull latest weather data and store it in SQLite.

```bash
python fetch_weather.py
```

## 3. Verify Database
Check that data was inserted correctly.

```bash
python -c "import sqlite3; conn = sqlite3.connect('data.db'); print(conn.execute('SELECT * FROM TemperatureForecasts LIMIT 5').fetchall())"
```

## 4. Run the Streamlit Web App
Launch the interactive dashboard locally.

```bash
streamlit run app.py
```

Open browser at: http://localhost:8501

## 5. Git — Stage & Commit Changes
After making changes, commit them with a meaningful message.

```bash
git add .
git commit -m "your message here"
```

## 6. Git — Push to GitHub
Push committed changes to the remote repository.

```bash
git push origin main
```

## 7. Full Update Cycle (fetch → verify → commit → push)
Run this sequence to update data and sync with GitHub.

```bash
python fetch_weather.py
git add .
git commit -m "Update weather data"
git push origin main
```
