CREATE TABLE IF NOT EXISTS analytics.dim_country (
    country_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    country_code VARCHAR(10) NOT NULL UNIQUE,
    country_name VARCHAR(150) NOT NULL,
    region VARCHAR(100),
    income_group VARCHAR(100),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS analytics.dim_indicator (
    indicator_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    indicator_code VARCHAR(150) NOT NULL UNIQUE,
    indicator_name VARCHAR(250) NOT NULL,
    domain VARCHAR(50) NOT NULL,
    unit VARCHAR(100),
    frequency VARCHAR(20),
    source_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS analytics.dim_period (
    period_key INTEGER PRIMARY KEY,
    year SMALLINT NOT NULL,
    quarter SMALLINT,
    month SMALLINT,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    UNIQUE (year, quarter, month)
);

COMMENT ON TABLE analytics.dim_country IS
'Canonical country dimension shared across economic, energy and trade models.';

COMMENT ON TABLE analytics.dim_indicator IS
'Canonical indicator metadata and source definitions.';

COMMENT ON TABLE analytics.dim_period IS
'Canonical time dimension supporting annual, quarterly and monthly observations.';
