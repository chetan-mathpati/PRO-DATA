with economic_data as (

    select *
    from {{ ref('int_country_economic_year') }}

),

with_change_metrics as (

    select
        *,
        lag(gdp_usd) over (
            partition by country_code
            order by year
        ) as previous_gdp_usd,

        lag(gdp_per_capita_usd) over (
            partition by country_code
            order by year
        ) as previous_gdp_per_capita_usd,

        avg(gdp_growth_pct) over (
            partition by country_code
            order by year
            rows between 4 preceding and current row
        ) as gdp_growth_5yr_avg,

        avg(inflation_pct) over (
            partition by country_code
            order by year
            rows between 4 preceding and current row
        ) as inflation_5yr_avg

    from economic_data

),

final as (

    select
        *,
        case
            when previous_gdp_usd is not null
                 and previous_gdp_usd <> 0
            then ((gdp_usd - previous_gdp_usd) / previous_gdp_usd) * 100
        end as gdp_yoy_change_pct,

        case
            when previous_gdp_per_capita_usd is not null
                 and previous_gdp_per_capita_usd <> 0
            then (
                (gdp_per_capita_usd - previous_gdp_per_capita_usd)
                / previous_gdp_per_capita_usd
            ) * 100
        end as gdp_per_capita_yoy_change_pct

    from with_change_metrics

)

select *
from final
