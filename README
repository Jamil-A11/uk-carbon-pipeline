# UK Grid Carbon Intensity Pipeline

An end-to-end data pipeline that ingests half-hourly carbon intensity data for Great Britain's electricity grid from the National Grid ESO API, and models it using a medallion (bronze / silver / gold) architecture.

## Key finding

In September 2026, electricity in Great Britain was cleanest around noon UK time (avg 74.5 g CO₂/kWh) and dirtiest around 7pm (avg 148.8 g CO₂/kWh), roughly twice as carbon-intensive. This means charging an electric car or running appliances at midday instead of the evening can halve their carbon footprint.

## Architecture

```
National Grid Carbon Intensity API
        │  ingestion/backfill.py      (Python: extract)
        ▼
data/bronze/*.json                    raw API responses, one file per day
        │  ingestion/load_bronze.py   (DuckDB SQL: load)
        ▼
warehouse.duckdb
├── bronze_national_intensity         1,440 rows  (one per half-hour)
└── bronze_regional_intensity        26,460 rows  (one per region per half-hour)
        │  dbt (coming next)
        ▼
silver → gold → dashboard
```

## Tech stack

Python (requests) · DuckDB · SQL · Git/GitHub
Planned: dbt · GitHub Actions (CI/CD) · Streamlit

## Data quality issues found

The regional table had 26,460 rows instead of the expected 25,920. Using a `GROUP BY ... HAVING` query, I found that the 23:30–00:00 period appeared in two files: once as the last period of one day, and again as the first period of the next. I kept the bronze layer unchanged so it remains a faithful copy of what the API returned and can be replayed if the cleaning logic changes, and will remove duplicates in the silver layer.

Also found:
- Timestamps arrive as text, not timestamps, so they will be cast in silver
- Regional data mixes 14 real regions with 4 aggregate rows (England, Scotland, Wales, GB), which would cause double counting if not separated
- Regional data includes forecasts only (no actual values)

## How to run

```bash
pip install -r requirements.txt
python ingestion/backfill.py      # fetch Sept 2026 into data/bronze/
python ingestion/load_bronze.py   # build bronze tables in data/warehouse.duckdb
```

## Status

- [x] Phase 1: Bronze ingestion (national + regional, September 2026)
- [ ] Phase 2: Silver cleaning with dbt + data tests
- [ ] Phase 3: Gold star schema + KPIs
- [ ] Phase 4: CI/CD with GitHub Actions
- [ ] Phase 5: Streamlit dashboard