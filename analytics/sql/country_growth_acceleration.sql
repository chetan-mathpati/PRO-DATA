WITH base AS (
    SELECT
        country_code,
        country_name,
        year,
        gdp_growth_pct,
        gdp_growth_5yr_avg,
        LAG(gdp_growth_pct) OVER (
            PARTITION BY country_code
            ORDER BY year
        ) AS previous_year_growth
    FROM analytics.mart_country_economic_energy
)
SELECT
    *,
    gdp_growth_pct - previous_year_growth
        AS growth_acceleration_pct_points
FROM base
WHERE year >= 2021
ORDER BY year DESC, growth_acceleration_pct_points DESC NULLS LAST;
