with years as (

    select distinct year
    from {{ ref('stg_world_bank_indicators') }}

)

select
    year as period_key,
    year,
    null::integer as quarter,
    null::integer as month,
    make_date(year::integer, 1, 1) as period_start,
    make_date(year::integer, 12, 31) as period_end
from years
