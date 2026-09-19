with base as (

    select *
    from {{ ref('int_country_economic_energy_year') }}

),

metrics as (

    select
        *,

        lag(total_petroleum_production_tbpd) over (
            partition by country_code
            order by year
        ) as previous_petroleum_production_tbpd,

        lag(crude_oil_production_tbpd) over (
            partition by country_code
            order by year
        ) as previous_crude_oil_production_tbpd,

        avg(gdp_growth_pct) over (
            partition by country_code
            order by year
            rows between 4 preceding and current row
        ) as gdp_growth_5yr_avg,

        avg(inflation_pct) over (
            partition by country_code
            order by year
            rows between 4 preceding and current row
        ) as inflation_5yr_avg,

        avg(total_petroleum_production_tbpd) over (
            partition by country_code
            order by year
            rows between 4 preceding and current row
        ) as petroleum_production_5yr_avg

    from base

)

select
    *,
    
    case
        when previous_petroleum_production_tbpd is not null
         and previous_petroleum_production_tbpd <> 0
        then (
            (
                total_petroleum_production_tbpd
                - previous_petroleum_production_tbpd
            )
            / previous_petroleum_production_tbpd
        ) * 100
    end as petroleum_production_yoy_pct,

    case
        when previous_crude_oil_production_tbpd is not null
         and previous_crude_oil_production_tbpd <> 0
        then (
            (
                crude_oil_production_tbpd
                - previous_crude_oil_production_tbpd
            )
            / previous_crude_oil_production_tbpd
        ) * 100
    end as crude_oil_production_yoy_pct,

    case
        when total_petroleum_production_tbpd is not null
         and total_petroleum_production_tbpd <> 0
         and crude_oil_production_tbpd is not null
        then (
            crude_oil_production_tbpd
            / total_petroleum_production_tbpd
        ) * 100
    end as crude_share_of_petroleum_production_pct

from metrics
