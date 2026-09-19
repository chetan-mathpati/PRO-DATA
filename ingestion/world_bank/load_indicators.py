from __future__ import annotations

import json
import logging
from pathlib import Path

import requests
from sqlalchemy import text

from warehouse.connection import create_engine_instance


PROJECT_ROOT = Path(__file__).resolve().parents[2]

API_BASE_URL = "https://api.worldbank.org/v2/country/all/indicator"

INDICATORS = {
    "NY.GDP.MKTP.CD": "GDP, current US$",
    "NY.GDP.MKTP.KD.ZG": "GDP growth (annual %)",
    "NY.GDP.PCAP.CD": "GDP per capita (current US$)",
    "FP.CPI.TOTL.ZG": "Inflation, consumer prices (annual %)",
    "SL.UEM.TOTL.ZS": "Unemployment, total (% of total labor force)",
    "NE.TRD.GNFS.ZS": "Trade (% of GDP)",
    "NE.EXP.GNFS.ZS": "Exports of goods and services (% of GDP)",
    "NE.IMP.GNFS.ZS": "Imports of goods and services (% of GDP)",
}

REQUEST_TIMEOUT = 60
PAGE_SIZE = 1000

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def fetch_indicator(indicator_code: str) -> list[dict]:
    """Fetch all available observations for one World Bank indicator."""

    page = 1
    records: list[dict] = []

    while True:
        params = {
            "format": "json",
            "per_page": PAGE_SIZE,
            "page": page,
        }

        url = f"{API_BASE_URL}/{indicator_code}"

        logger.info(
            "Fetching %s | page=%s",
            indicator_code,
            page,
        )

        response = requests.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        payload = response.json()

        if not isinstance(payload, list) or len(payload) < 2:
            raise RuntimeError(
                f"Unexpected World Bank response for {indicator_code}"
            )

        metadata = payload[0]
        observations = payload[1]

        records.extend(observations)

        total_pages = int(metadata["pages"])

        logger.info(
            "Fetched %s rows | page %s/%s",
            len(observations),
            page,
            total_pages,
        )

        if page >= total_pages:
            break

        page += 1

    return records


def normalize_records(
    indicator_code: str,
    observations: list[dict],
) -> list[dict]:
    """Convert World Bank observations into warehouse-ready records."""

    normalized = []

    source_url = f"{API_BASE_URL}/{indicator_code}"

    for observation in observations:
        country = observation.get("country") or {}
        indicator = observation.get("indicator") or {}

        country_code = observation.get("countryiso3code")
        year_text = observation.get("date")
        value = observation.get("value")

        if not country_code or not year_text:
            continue

        try:
            year = int(year_text)
        except ValueError:
            continue

        numeric_value = None

        if value is not None:
            try:
                numeric_value = float(value)
            except (TypeError, ValueError):
                numeric_value = None

        normalized.append(
            {
                "country_code": country_code,
                "country_name": country.get("value"),
                "indicator_code": indicator_code,
                "indicator_name": indicator.get("value"),
                "year": year,
                "value": numeric_value,
                "source_url": source_url,
                "source_payload": json.dumps(observation),
            }
        )

    return normalized


def load_records(records: list[dict]) -> None:
    """Upsert normalized records into the raw warehouse layer."""

    if not records:
        return

    engine = create_engine_instance()

    sql = text(
        """
        INSERT INTO raw.world_bank_indicators (
            country_code,
            country_name,
            indicator_code,
            indicator_name,
            year,
            value,
            source_url,
            source_payload
        )
        VALUES (
            :country_code,
            :country_name,
            :indicator_code,
            :indicator_name,
            :year,
            :value,
            :source_url,
            CAST(:source_payload AS JSONB)
        )
        ON CONFLICT (
            country_code,
            indicator_code,
            year
        )
        DO UPDATE SET
            country_name = EXCLUDED.country_name,
            indicator_name = EXCLUDED.indicator_name,
            value = EXCLUDED.value,
            source_url = EXCLUDED.source_url,
            source_payload = EXCLUDED.source_payload,
            fetched_at = CURRENT_TIMESTAMP
        """
    )

    try:
        with engine.begin() as connection:
            connection.execute(sql, records)
    finally:
        engine.dispose()


def main() -> None:
    total_loaded = 0

    for indicator_code in INDICATORS:
        observations = fetch_indicator(indicator_code)

        records = normalize_records(
            indicator_code,
            observations,
        )

        load_records(records)

        logger.info(
            "Loaded %s records for %s",
            len(records),
            indicator_code,
        )

        total_loaded += len(records)

    logger.info(
        "World Bank ingestion complete | total records=%s",
        total_loaded,
    )


if __name__ == "__main__":
    main()
