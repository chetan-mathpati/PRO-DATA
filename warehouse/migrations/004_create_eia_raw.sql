CREATE TABLE IF NOT EXISTS raw.eia_energy (
    country_code VARCHAR(10) NOT NULL,
    country_name VARCHAR(150),
    series_id VARCHAR(200) NOT NULL,
    series_name VARCHAR(300),
    period VARCHAR(20) NOT NULL,
    value NUMERIC(24,8),
    unit VARCHAR(100),
    source_url TEXT NOT NULL,
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    source_payload JSONB,

    PRIMARY KEY (country_code, series_id, period)
);

COMMENT ON TABLE raw.eia_energy IS
'Source-aligned international energy observations from the U.S. Energy Information Administration.';

COMMENT ON COLUMN raw.eia_energy.source_payload IS
'Original API observation retained for traceability.';
