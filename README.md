# 🌍 Global Capitals Real-time Weather Data (2025)

This dataset contains **real-time and near real-time weather observations** from world capitals, collected during **November 2025**.

Each row represents one observation of weather conditions for a capital city in UTC and local time.

---

## 📊 Dataset Structure

| Column | Description |
|---------|--------------|
| `utc_time` | Time of observation in UTC |
| `local_time` | Local time in the capital |
| `country` | Country name |
| `capital` | Capital city name |
| `continent` | Continent of the country |
| `temperature` | Current temperature (°C) |
| `temp_min` / `temp_max` | Minimum and maximum temperatures (°C) |
| `humidity` | Relative humidity (%) |
| `feels_like` | Feels-like temperature (°C) |
| `visibility` | Visibility distance (m) |
| `precipitation` | Precipitation in mm |
| `cloudcover` | Cloud cover (%) |
| `wind_speed` / `wind_gust` | Wind speed and gust (m/s) |
| `wind_direction` | Wind direction in degrees |
| `pressure` | Atmospheric pressure (hPa) |
| `is_day` | 1 = daytime, 0 = night |
| `weather_code` | Weather condition code |
| `weather_main` | Main weather condition (e.g., Clouds, Clear, Rain) |
| `weather_description` | Detailed description |
| `weather_icon` | Icon code from OpenWeather API |

---

## 🗺️ Coverage

- **Countries:** All sovereign nations (≈195)
- **Capitals:** One per country
- **Time span:** November 2025 (hourly or 3-hour interval updates)
- **Source:** Collected via Open-Meteo API / PythonAnywhere cron job

---

## 💡 Usage Ideas

- Global weather visualization dashboards  
- Climate comparison by continent  
- Model training for temperature or humidity prediction  
- Educational use in data science and meteorology courses  

---

## ⚙️ Technical Info

- Format: CSV (UTF-8)
- Encoding: Standard ASCII, comma-separated
- Missing values: Represented by `NaN` or `Unknown`

---

## 🧾 License

CC BY 4.0 — you may use this data with attribution.

---

## ✍️ Author

Dataset curated by [your Kaggle username].  
Maintained on [PythonAnywhere](https://www.pythonanywhere.com/) with hourly updates.
