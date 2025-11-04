# 🌍 Capital Weather Tracker

A curated collection of near real-time weather observations for world capitals, updated throughout November 2025. This repository combines the raw dataset with the Python tooling used to fetch, enrich, and maintain the data, enabling analysts and educators to explore current climate conditions across the globe.

---

## 📚 Table of Contents
1. [Project Overview](#-project-overview)
2. [Dataset Highlights](#-dataset-highlights)
3. [Repository Structure](#-repository-structure)
4. [Getting Started](#-getting-started)
5. [Using the Dataset](#-using-the-dataset)
6. [Automation & Update Pipeline](#-automation--update-pipeline)
7. [Contributing](#-contributing)
8. [License](#-license)
9. [Maintainer](#-maintainer)

---

## 🧭 Project Overview
- **Scope:** Weather metrics for the capital city of every sovereign country (~195 records per run).
- **Cadence:** Hourly or three-hourly snapshots collected during November 2025.
- **Sources:** Open-Meteo APIs orchestrated through Python scripts scheduled on PythonAnywhere.
- **Purpose:** Provide a reliable, ready-to-use dataset for dashboards, machine learning experiments, and classroom demonstrations in climatology or data science.

---

## ✨ Dataset Highlights
| Column | Description |
|--------|-------------|
| `utc_time` / `local_time` | Observation timestamps in UTC and local time. |
| `country`, `capital`, `continent` | Geospatial identifiers for each record. |
| `temperature`, `temp_min`, `temp_max`, `feels_like` | Core thermal indicators in °C. |
| `humidity`, `visibility`, `cloudcover`, `precipitation` | Atmospheric conditions capturing moisture, clarity, and precipitation intensity. |
| `wind_speed`, `wind_gust`, `wind_direction` | Wind metrics in m/s and degrees. |
| `pressure` | Sea-level pressure in hPa. |
| `is_day` | Daylight flag (1 = daytime, 0 = nighttime). |
| `weather_code`, `weather_main`, `weather_description`, `weather_icon` | Condition codes sourced from the Open-Meteo/OpenWeather taxonomy. |

Missing values are represented by `NaN` or `Unknown`, and the dataset is stored as UTF-8 CSV.

---

## 🗂️ Repository Structure
```
├── Countries-v1/                # Static country reference tables
├── Images/                      # Visual assets for documentation and dashboards
├── data/                        # Exported weather datasets (CSV files)
├── src/
│   ├── config/                  # Configuration files and constants
│   └── script/                  # ETL scripts powering the data pipeline
│       ├── weather_countries_collector.py
│       ├── add_continent.py
│       ├── merge_countries_csv.py
│       └── delete_bak_files.py
├── requirements.txt             # Python dependencies for the tooling
└── README.md
```

---

## 🚀 Getting Started
1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/capital-weather-tracker.git
   cd capital-weather-tracker
   ```
2. **Create and activate a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\\Scripts\\activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables** (if required by the API keys in your workflow).

---

## 📈 Using the Dataset
Load the latest CSV into a pandas DataFrame and start exploring:

```python
import pandas as pd

df = pd.read_csv("data/capital_weather_latest.csv")
print(df.head())
```

Example analysis ideas:
- Build interactive dashboards comparing continents or climate zones.
- Train predictive models for temperature, humidity, or wind speed.
- Demonstrate ETL best practices in workshops or university courses.

---

## 🔄 Automation & Update Pipeline
The automation scripts in `src/script/` manage the end-to-end lifecycle:

1. **`weather_countries_collector.py`** — Queries the Open-Meteo API for every capital and stores the raw observations.
2. **`add_continent.py`** — Enriches records with continent metadata from reference tables.
3. **`merge_countries_csv.py`** — Consolidates outputs into a single analytics-friendly CSV.
4. **`delete_bak_files.py`** — Cleans temporary files to keep storage tidy.

Schedule these scripts via cron (e.g., on PythonAnywhere) to keep the dataset refreshed.

---

## 🤝 Contributing
Contributions that improve data quality, expand automation, or enhance documentation are welcome! Please open an issue or submit a pull request describing your changes.

---

## 🧾 License
This project is distributed under the **CC BY 4.0** license. Feel free to use the data and tooling with attribution.

---

## 👤 Maintainer
Curated and maintained by **[@lduyhi]**, with automated jobs running on [PythonAnywhere](https://www.pythonanywhere.com/).
