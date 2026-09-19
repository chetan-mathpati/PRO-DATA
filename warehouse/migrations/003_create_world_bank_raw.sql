CREATE TABLE IF NOT EXISTS raw.world_bank_indicators (
    country_code VARCHAR(10) NOT NULL,
    country_name VARCHAR(150),
    indicator_code VARCHAR(150) NOT NULL,
    indicator_name VARCHAR(250),
    year SMALLINT NOT NULL,
    value NUMERIC(24,8),
    source_url TEXT NOT NULL,
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    source_payload JSONB,

    PRIMARY KEY (country_code, indicator_code, year)
);

COMMENT ON TABLE raw.world_bank_indicators IS
'Source-aligned World Bank indicator observations.';

COMMENT ON COLUMN raw.world_bank_indicators.source_payload IS
'Original API observation retained for traceability.';
