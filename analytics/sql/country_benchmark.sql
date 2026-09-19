with latest_year as (
    select max(year) as year
    from analytics.mart_country_economic_energy
),
base as (
    select
        m.country_code,
        m.country_name,
        m.year,
        m.gdp_usd,
        m.gdp_per_capita_usd,
        m.gdp_growth_pct,
        m.inflation_pct,
        m.unemployment_pct,
        m.trade_pct_gdp,
        m.total_petroleum_production_tbpd,
        m.crude_oil_production_tbpd,
        m.petroleum_consumption_tj
    from analytics.mart_country_economic_energy m
    join latest_year y
      on m.year = y.year
),
benchmarks as (
    select
        *,
        percentile_cont(0.50) within group (
            order by gdp_per_capita_usd
        ) over () as global_median_gdp_per_capita,
        percentile_cont(0.50) within group (
            order by gdp_growth_pct
        ) over () as global_median_growth,
        percentile_cont(0.50) within group (
            order by inflation_pct
        ) over () as global_median_inflation
    from base
)
select
    *,
    case
        when gdp_per_capita_usd is not null
        then gdp_per_capita_usd / nullif(global_median_gdp_per_capita, 0)
    end as gdp_per_capita_vs_global_median_ratio,

    case
        when gdp_growth_pct is not null
        then gdp_growth_pct - global_median_growth
    end as growth_vs_global_median_pct_points,

    case
        when inflation_pct is not null
        then inflation_pct - global_median_inflation
    end as inflation_vs_global_median_pct_points
from benchmarks
order by country_name;