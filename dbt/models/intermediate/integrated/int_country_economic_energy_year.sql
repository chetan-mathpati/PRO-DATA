with economic as (

    select *
    from {{ ref('int_country_economic_year') }}

),

energy as (

    select
        country_code,
        country_name,
        period::integer as year,

        max(
            case
                when product_id = '53'
                 and activity_id = '1'
                then value
            end
        ) as total_petroleum_production_tbpd,

        max(
            case
                when product_id = '57'
                 and activity_id = '1'
                then value
            end
        ) as crude_oil_production_tbpd,

        max(
            case
                when product_id = '5'
                 and activity_id = '2'
                then value
            end
        ) as petroleum_consumption_tj

    from {{ ref('stg_eia_energy') }}

    group by
        country_code,
        country_name,
        period

)

select
    e.country_code,
    e.country_name,
    e.year,

    e.gdp_usd,
    e.gdp_growth_pct,
    e.gdp_per_capita_usd,
    e.inflation_pct,
    e.unemployment_pct,
    e.trade_pct_gdp,
    e.exports_pct_gdp,
    e.imports_pct_gdp,

    en.total_petroleum_production_tbpd,
    en.crude_oil_production_tbpd,
    en.petroleum_consumption_tj

from economic e

left join energy en
    on e.country_code = en.country_code
   and e.year = en.year
