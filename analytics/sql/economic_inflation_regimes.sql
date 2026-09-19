WITH base AS (
    SELECT
        country_code,
        country_name,
        year,
        gdp_growth_pct,
        inflation_pct
    FROM analytics.mart_country_economic_energy
),
year_stats AS (
    SELECT
        year,
        percentile_cont(0.50) WITHIN GROUP (
            ORDER BY gdp_growth_pct
        ) AS median_gdp_growth,
        percentile_cont(0.50) WITHIN GROUP (
            ORDER BY inflation_pct
        ) AS median_inflation
    FROM base
    WHERE gdp_growth_pct IS NOT NULL
      AND inflation_pct IS NOT NULL
    GROUP BY year
)
SELECT
    b.*,
    s.median_gdp_growth,
    s.median_inflation,
    CASE
        WHEN b.gdp_growth_pct >= s.median_gdp_growth
         AND b.inflation_pct < s.median_inflation
            THEN 'higher_growth_lower_inflation'
        WHEN b.gdp_growth_pct >= s.median_gdp_growth
         AND b.inflation_pct >= s.median_inflation
            THEN 'higher_growth_higher_inflation'
        WHEN b.gdp_growth_pct < s.median_gdp_growth
         AND b.inflation_pct < s.median_inflation
            THEN 'lower_growth_lower_inflation'
        WHEN b.gdp_growth_pct < s.median_gdp_growth
         AND b.inflation_pct >= s.median_inflation
            THEN 'lower_growth_higher_inflation'
        ELSE 'unclassified'
    END AS economic_regime
FROM base b
LEFT JOIN year_stats s
    ON b.year = s.year
WHERE b.year >= 2021
ORDER BY b.year DESC, b.country_code;
