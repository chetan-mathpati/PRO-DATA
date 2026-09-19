import os
import json
import logging
from datetime import datetime, timezone

import requests
import psycopg
from dotenv import load_dotenv

load_dotenv(".env", override=True)

EIA_API_KEY = os.getenv("EIA_API_KEY")

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
DB_NAME = os.getenv("POSTGRES_DB", "pro_data")
DB_USER = os.getenv("POSTGRES_USER", "pro_data")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

BASE_URL = "https://api.eia.gov/v2/international/data/"
START_YEAR = "2000"
END_YEAR = "2025"
PAGE_SIZE = 5000

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def api(params):
    params = dict(params)
    params["api_key"] = EIA_API_KEY

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=60
    )
    response.raise_for_status()

    payload = response.json()

    if "response" not in payload:
        raise RuntimeError(json.dumps(payload)[:2000])

    return payload["response"]


def test_combination(product_id, activity_id):
    response = api({
        "frequency": "annual",
        "data[0]": "value",
        "facets[productId][]": product_id,
        "facets[activityId][]": activity_id,
        "facets[countryRegionTypeId][]": "c",
        "start": "2024",
        "end": "2024",
        "length": 1,
    })

    return int(response.get("total", 0))


def fetch_activity(product_id, product_name, activity_id, activity_name):
    rows = []
    offset = 0

    while True:
        response = api({
            "frequency": "annual",
            "data[0]": "value",
            "facets[productId][]": product_id,
            "facets[activityId][]": activity_id,
            "facets[countryRegionTypeId][]": "c",
            "start": START_YEAR,
            "end": END_YEAR,
            "sort[0][column]": "period",
            "sort[0][direction]": "asc",
            "offset": offset,
            "length": PAGE_SIZE,
        })

        batch = response.get("data", [])

        if not batch:
            break

        rows.extend(batch)

        total = response.get("total", "?")

        logging.info(
            "%s / %s: %s rows | total=%s",
            activity_name,
            product_name,
            len(rows),
            total
        )

        if len(batch) < PAGE_SIZE:
            break

        offset += PAGE_SIZE

    return rows


def normalize_value(value):
    """
    Convert EIA sentinel/malformed values into SQL-safe numeric values.

    EIA may return '--' when an observation is unavailable.
    The original source row remains preserved in source_payload.
    """

    if value is None:
        return None

    if isinstance(value, (int, float)):
        return value

    value = str(value).strip()

    if value in {"", "--", "NA", "N/A", "null", "None"}:
        return None

    try:
        return float(value)
    except ValueError:
        return None


def recreate_table(conn):
    logging.info("Recreating raw.eia_energy")

    conn.execute("""
        DROP TABLE IF EXISTS raw.eia_energy;

        CREATE TABLE raw.eia_energy (
            country_code VARCHAR(20) NOT NULL,
            country_name VARCHAR(150),
            product_id VARCHAR(50) NOT NULL,
            product_name VARCHAR(300),
            activity_id VARCHAR(50) NOT NULL,
            activity_name VARCHAR(150),
            period VARCHAR(20) NOT NULL,
            value NUMERIC(24,8),
            unit VARCHAR(100),
            source_url TEXT NOT NULL,
            fetched_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            source_payload JSONB,
            PRIMARY KEY (
                country_code,
                product_id,
                activity_id,
                period
            )
        );

        COMMENT ON TABLE raw.eia_energy IS
        'Source-aligned annual international petroleum and liquids observations from EIA.';

        COMMENT ON COLUMN raw.eia_energy.value IS
        'Numeric EIA observation. Source sentinel values such as -- are normalized to NULL.';

        COMMENT ON COLUMN raw.eia_energy.source_payload IS
        'Original EIA observation retained for source traceability.';
    """)


def load_rows(conn, rows):
    sql = """
        INSERT INTO raw.eia_energy (
            country_code,
            country_name,
            product_id,
            product_name,
            activity_id,
            activity_name,
            period,
            value,
            unit,
            source_url,
            fetched_at,
            source_payload
        )
        VALUES (
            %(country_code)s,
            %(country_name)s,
            %(product_id)s,
            %(product_name)s,
            %(activity_id)s,
            %(activity_name)s,
            %(period)s,
            %(value)s,
            %(unit)s,
            %(source_url)s,
            %(fetched_at)s,
            %(source_payload)s
        )
        ON CONFLICT (
            country_code,
            product_id,
            activity_id,
            period
        )
        DO UPDATE SET
            country_name = EXCLUDED.country_name,
            product_name = EXCLUDED.product_name,
            activity_name = EXCLUDED.activity_name,
            value = EXCLUDED.value,
            unit = EXCLUDED.unit,
            source_url = EXCLUDED.source_url,
            fetched_at = EXCLUDED.fetched_at,
            source_payload = EXCLUDED.source_payload;
    """

    now = datetime.now(timezone.utc)
    prepared = []
    normalized_nulls = 0

    for row in rows:

        country_code = row.get("countryRegionId")

        if not country_code:
            continue

        raw_value = row.get("value")
        value = normalize_value(raw_value)

        if raw_value is not None and value is None:
            normalized_nulls += 1

        prepared.append({
            "country_code": country_code,
            "country_name": row.get("countryRegionName"),
            "product_id": row.get("productId"),
            "product_name": row.get("productName"),
            "activity_id": row.get("activityId"),
            "activity_name": row.get("activityName"),
            "period": row.get("period"),
            "value": value,
            "unit": row.get("unit"),
            "source_url": BASE_URL,
            "fetched_at": now,
            "source_payload": json.dumps(row),
        })

    with conn.cursor() as cursor:
        cursor.executemany(sql, prepared)

    return len(prepared), normalized_nulls


def main():

    if not EIA_API_KEY:
        raise RuntimeError("EIA_API_KEY is missing")

    print("=" * 80)
    print("PRO DATA — EIA ENERGY INGESTION")
    print("=" * 80)

    candidates = [
        ("5", "Petroleum and other liquids", "2", "Consumption"),
        ("53", "Total petroleum and other liquids", "1", "Production"),
        ("57", "Crude oil including lease condensate", "1", "Production"),
    ]

    print("\nValidating EIA combinations...")
    print("-" * 80)

    valid = []

    for product_id, product_name, activity_id, activity_name in candidates:

        total = test_combination(
            product_id,
            activity_id
        )

        print(
            f"{product_id:>3} | "
            f"{product_name:<40} | "
            f"{activity_name:<12} | "
            f"2024 rows={total}"
        )

        if total > 0:
            valid.append(
                (
                    product_id,
                    product_name,
                    activity_id,
                    activity_name
                )
            )

    with psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    ) as conn:

        recreate_table(conn)

        total_loaded = 0
        total_normalized_nulls = 0

        for (
            product_id,
            product_name,
            activity_id,
            activity_name
        ) in valid:

            rows = fetch_activity(
                product_id,
                product_name,
                activity_id,
                activity_name
            )

            loaded, normalized_nulls = load_rows(
                conn,
                rows
            )

            total_loaded += loaded
            total_normalized_nulls += normalized_nulls

            logging.info(
                "Loaded %s rows | normalized %s unavailable values | %s / %s",
                loaded,
                normalized_nulls,
                product_name,
                activity_name
            )

        conn.commit()

        print("\n" + "=" * 80)
        print("EIA VALIDATION")
        print("=" * 80)

        summary = conn.execute("""
            SELECT
                activity_name,
                product_id,
                product_name,
                COUNT(*) AS rows,
                COUNT(DISTINCT country_code) AS countries,
                MIN(period) AS first_period,
                MAX(period) AS last_period,
                COUNT(*) FILTER (
                    WHERE value IS NULL
                ) AS null_values
            FROM raw.eia_energy
            GROUP BY
                activity_name,
                product_id,
                product_name
            ORDER BY
                activity_name,
                product_id;
        """).fetchall()

        for r in summary:
            print(
                f"{r[0]:12} | "
                f"{r[1]:>3} | "
                f"{r[2][:35]:35} | "
                f"rows={r[3]:7} | "
                f"countries={r[4]:4} | "
                f"{r[5]} -> {r[6]} | "
                f"nulls={r[7]}"
            )

        duplicates = conn.execute("""
            SELECT COUNT(*)
            FROM (
                SELECT
                    country_code,
                    product_id,
                    activity_id,
                    period
                FROM raw.eia_energy
                GROUP BY
                    country_code,
                    product_id,
                    activity_id,
                    period
                HAVING COUNT(*) > 1
            ) x;
        """).fetchone()[0]

        print("\nDuplicate business keys:", duplicates)

        india = conn.execute("""
            SELECT
                country_code,
                country_name,
                product_name,
                activity_name,
                period,
                value,
                unit
            FROM raw.eia_energy
            WHERE country_code = 'IND'
            ORDER BY period DESC, activity_name
            LIMIT 15;
        """).fetchall()

        print("\nIndia sample:")
        for row in india:
            print(row)

        print("\nTotal rows loaded:", total_loaded)
        print(
            "Unavailable source values normalized to NULL:",
            total_normalized_nulls
        )

        print("=" * 80)


if __name__ == "__main__":
    main()
