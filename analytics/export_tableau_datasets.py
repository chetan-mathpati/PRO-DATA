import os
from pathlib import Path

import pandas as pd
import psycopg
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "analytics" / "exports"
OUTPUT.mkdir(parents=True, exist_ok=True)

conninfo = (
    f"host={os.getenv('POSTGRES_HOST', 'localhost')} "
    f"port={os.getenv('POSTGRES_PORT', '5432')} "
    f"dbname={os.getenv('POSTGRES_DB', 'pro_data')} "
    f"user={os.getenv('POSTGRES_USER', 'pro_data')} "
    f"password={os.getenv('POSTGRES_PASSWORD')}"
)

queries = {
    "global_economic_energy": """
        SELECT *
        FROM analytics.mart_country_economic_energy
        ORDER BY country_code, year
    """,

    "country_benchmark": """
        SELECT *
        FROM analytics.mart_country_economic_energy
        WHERE year = (
            SELECT MAX(year)
            FROM analytics.mart_country_economic_energy
        )
        ORDER BY country_name
    """,

    "energy_signals": """
        SELECT
            *,
            CASE
                WHEN total_petroleum_production_tbpd IS NOT NULL
                 AND petroleum_production_5yr_avg IS NOT NULL
                 AND total_petroleum_production_tbpd
                     < petroleum_production_5yr_avg * 0.90
                    THEN 'production_below_trend'

                WHEN petroleum_production_yoy_pct <= -10
                    THEN 'sharp_production_decline'

                ELSE 'normal_or_insufficient_data'
            END AS energy_signal

        FROM analytics.mart_country_economic_energy
        WHERE year >= 2021
        ORDER BY country_code, year
    """,
}

with psycopg.connect(conninfo) as conn:
    for name, query in queries.items():
        df = pd.read_sql_query(query, conn)

        path = OUTPUT / f"{name}.csv"
        df.to_csv(path, index=False)

        print(
            f"{name}: {len(df):,} rows -> {path}"
        )

print("TABLEAU DATA EXPORT COMPLETE")
