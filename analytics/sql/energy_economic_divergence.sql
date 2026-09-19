WITH base AS (
    SELECT
        country_code,
        country_name,
        year,
        gdp_growth_pct,
        total_petroleum_production_tbpd,
        petroleum_production_yoy_pct,
        petroleum_consumption_tj,
        crude_oil_production_tbpd,
        crude_share_of_petroleum_production_pct
    FROM analytics.mart_country_economic_energy
)
SELECT
    *,
    CASE
        WHEN gdp_growth_pct > 0
         AND petroleum_production_yoy_pct < 0
            THEN 'growth_up_production_down'
        WHEN gdp_growth_pct < 0
         AND petroleum_production_yoy_pct > 0
            THEN 'growth_down_production_up'
        WHEN gdp_growth_pct > 0
         AND petroleum_production_yoy_pct > 0
            THEN 'growth_up_production_up'
        WHEN gdp_growth_pct < 0
         AND petroleum_production_yoy_pct < 0
            THEN 'growth_down_production_down'
        ELSE 'mixed_or_missing'
    END AS economic_energy_signal
FROM base
WHERE year >= 2021
ORDER BY year DESC, country_code;
