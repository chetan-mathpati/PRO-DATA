CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS analytics;

COMMENT ON SCHEMA raw IS 'Source-aligned data loaded from external providers.';
COMMENT ON SCHEMA staging IS 'Cleaned and standardized source data.';
COMMENT ON SCHEMA analytics IS 'Business-ready models used by analytics and reporting.';
