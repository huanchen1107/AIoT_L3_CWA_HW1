import sqlite3
import pandas as pd

conn = sqlite3.connect('data.db')
df = pd.read_sql_query("SELECT forecast_start, forecast_end, weather, min_temp, max_temp, rain_probability FROM weather_forecasts WHERE location_name='新竹縣' LIMIT 5", conn)
print(df.to_string(index=False))
conn.close()
