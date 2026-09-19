import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

conninfo = (
    f"host={os.getenv('POSTGRES_HOST', 'localhost')} "
    f"port={os.getenv('POSTGRES_PORT', '5432')} "
    f"dbname={os.getenv('POSTGRES_DB', 'pro_data')} "
    f"user={os.getenv('POSTGRES_USER', 'pro_data')} "
    f"password={os.getenv('POSTGRES_PASSWORD')}"
)

checks = {
    "raw_world_bank": (
        "SELECT COUNT(*) FROM raw.world_bank_indicators"
    ),
    "raw_eia": (
        "SELECT COUNT(*) FROM raw.eia_energy"
    ),
    "integrated_mart": (
        "SELECT COUNT(*) "
        "FROM analytics.mart_country_economic_energy"
    ),
    "countries": (
        "SELECT COUNT(*) FROM analytics.dim_country"
    ),
    "indicators": (
        "SELECT COUNT(*) FROM analytics.dim_indicator"
    ),
    "periods": (
        "SELECT COUNT(*) FROM analytics.dim_period"
    ),
    "integrated_duplicates": (
        "SELECT COUNT(*) "
        "FROM ("
        "SELECT country_code, year "
        "FROM analytics.mart_country_economic_energy "
        "GROUP BY country_code, year "
        "HAVING COUNT(*) > 1"
        ") x"
    ),
}

with psycopg.connect(conninfo) as conn:
    for name, query in checks.items():
        value = conn.execute(query).fetchone()[0]
        print(f"{name}: {value:,}")

print()
print("PROJECT DATABASE VALIDATION COMPLETE")
