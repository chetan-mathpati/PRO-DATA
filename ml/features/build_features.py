import os
from pathlib import Path

import pandas as pd
import psycopg
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "ml" / "features" / "country_energy_features.csv"

conninfo = (
    f"host={os.getenv('POSTGRES_HOST', 'localhost')} "
    f"port={os.getenv('POSTGRES_PORT', '5432')} "
    f"dbname={os.getenv('POSTGRES_DB', 'pro_data')} "
    f"user={os.getenv('POSTGRES_USER', 'pro_data')} "
    f"password={os.getenv('POSTGRES_PASSWORD')}"
)

QUERY = """
WITH base AS (
    SELECT
        country_code,
        country_name,
        year,
        gdp_growth_pct,
        inflation_pct,
        unemployment_pct,
        trade_pct_gdp,
        exports_pct_gdp,
        imports_pct_gdp,
        total_petroleum_production_tbpd,
        crude_oil_production_tbpd,
        petroleum_consumption_tj,
        petroleum_production_yoy_pct,
        crude_oil_production_yoy_pct,
        gdp_growth_5yr_avg,
        inflation_5yr_avg,
        petroleum_production_5yr_avg,

        LAG(total_petroleum_production_tbpd)
            OVER (
                PARTITION BY country_code
                ORDER BY year
            ) AS previous_production,

        LAG(total_petroleum_production_tbpd, 2)
            OVER (
                PARTITION BY country_code
                ORDER BY year
            ) AS production_two_years_ago,

        LEAD(total_petroleum_production_tbpd)
            OVER (
                PARTITION BY country_code
                ORDER BY year
            ) AS next_year_production

    FROM analytics.mart_country_economic_energy
)
SELECT
    *,
    CASE
        WHEN next_year_production IS NOT NULL
         AND total_petroleum_production_tbpd IS NOT NULL
         AND total_petroleum_production_tbpd <> 0
        THEN (
            (next_year_production - total_petroleum_production_tbpd)
            / total_petroleum_production_tbpd
        ) * 100
    END AS next_year_production_change_pct,

    CASE
        WHEN next_year_production IS NOT NULL
         AND total_petroleum_production_tbpd IS NOT NULL
         AND next_year_production
             < total_petroleum_production_tbpd * 0.90
            THEN 1
        WHEN next_year_production IS NOT NULL
            THEN 0
    END AS next_year_production_decline_target

FROM base
WHERE year <= (
    SELECT MAX(year) - 1
    FROM analytics.mart_country_economic_energy
)
ORDER BY country_code, year;
"""

with psycopg.connect(conninfo) as conn:
    df = pd.read_sql_query(QUERY, conn)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT, index=False)

print(f"Feature rows: {len(df):,}")
print(f"Feature columns: {len(df.columns)}")
print(f"Output: {OUTPUT}")
print(
    "Target distribution:",
    df["next_year_production_decline_target"]
    .value_counts(dropna=False)
    .to_dict()
)
