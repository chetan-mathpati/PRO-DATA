WITH base AS (
    SELECT
        country_code,
        country_name,
        year,
        gdp_growth_pct,
        petroleum_production_5yr_avg,
        total_petroleum_production_tbpd,
        crude_oil_production_tbpd,
        petroleum_consumption_tj,
        petroleum_production_yoy_pct,
        crude_share_of_petroleum_production_pct
    FROM analytics.mart_country_economic_energy
)

SELECT
    *,
    
    CASE
        WHEN total_petroleum_production_tbpd IS NULL
          OR petroleum_production_5yr_avg IS NULL
            THEN NULL
        WHEN total_petroleum_production_tbpd
             < petroleum_production_5yr_avg * 0.90
            THEN TRUE
        ELSE FALSE
    END AS production_below_five_year_average,

    CASE
        WHEN petroleum_production_yoy_pct IS NULL
            THEN NULL
        WHEN petroleum_production_yoy_pct <= -10
            THEN TRUE
        ELSE FALSE
    END AS sharp_production_decline,

    CASE
        WHEN crude_share_of_petroleum_production_pct IS NULL
            THEN NULL
        WHEN crude_share_of_petroleum_production_pct >= 75
            THEN TRUE
        ELSE FALSE
    END AS high_crude_concentration

FROM base
WHERE year >= 2021
ORDER BY year DESC, country_code;