# Mini Data Pipeline & Weather Analytics (ETL)

A practical end-to-end Data Engineering project demonstrating both **Batch Processing (CSV)** and **Real-time API Ingestion (REST API)** with SQLite and Data Visualization.

---

## 📊 Weather Forecast Dashboard (Phitsanulok)
The pipeline extracts real-time 24-hour weather data from the Open-Meteo API, stores it in SQLite, and generates an automated visualization:

[weather_chart.png]

---

## 🛠️ Tech Stack & Skills
- **Language:** Python 3.13
- **Data Ingestion:** REST API (`requests`), CSV File processing
- **Data Processing:** `pandas` (Cleaning, Filtering, Transformation)
- **Database:** `sqlite3` (Relational Database Storage & SQL Analytics)
- **Visualization:** `matplotlib` (Automated Trend Chart Generation)
- **Version Control:** Git & GitHub

---

## 🚀 Pipelines Overview

### 1. Phitsanulok Weather Pipeline (`weather_pipeline.py` & `visualize_weather.py`)
- **Extract:** Fetches real-time weather & 24-hour forecast data for Phitsanulok (Lat: 16.82, Long: 100.26) from Open-Meteo API.
- **Transform:** Converts weather codes to descriptive labels and prepares time-series records.
- **Load:** Appends records incrementally into `weather.db` (`phitsanulok_weather` and `weather_24h_forecast` tables).
- **Visualize:** Queries data using SQL and exports `weather_chart.png`.

### 2. Sales Transaction Pipeline (`pipeline.py`)
- **Extract:** Reads batch transactions from `raw_sales.csv`.
- **Transform:** Performs data quality validation (filtering out invalid negative prices).
- **Load:** Saves cleaned records into `sales.db`.
- **Analytics:** Runs aggregated SQL queries for customer purchase summary.

---

## How to Run

1. **Install dependencies:**
   ```bash
   pip install pandas requests matplotlib