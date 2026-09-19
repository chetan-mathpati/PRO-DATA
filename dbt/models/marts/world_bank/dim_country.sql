with countries as (

    select
        country_code,
        max(country_name) as country_name
    from {{ ref('stg_world_bank_indicators') }}
    where country_code is not null
    group by country_code

)

select
    row_number() over (order by country_code) as country_key,
    country_code,
    country_name,
    true as is_active
from countries
