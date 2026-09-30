# Mini Data Pipeline (ETL with Python & SQLite)

A simple, end-to-end ETL data pipeline project demonstrating core Data Engineering and Data Quality Testing concepts.

## Tech Stack
- **Python 3.13**
- **Pandas** (Data Transformation & Filtering)
- **SQLite** (Relational Database Storage)
- **SQL** (Aggregation & Reporting Query)

## Pipeline Workflow
1. **Extract:** Ingests raw sales transaction data from a CSV file (`raw_sales.csv`).
2. **Transform (Data Quality Check):** Cleans the dataset by filtering out invalid and negative pricing anomalies (`price > 0`).
3. **Load:** Automatically creates and inserts cleaned records into the `orders` table in SQLite (`sales.db`).
4. **Verify / Analytics:** Runs an aggregated SQL query to calculate the total amount spent per customer.

## How to Run
```bash
pip install pandas
python pipeline.py