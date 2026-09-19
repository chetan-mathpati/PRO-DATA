with source_data as (

    select
        country_code,
        country_name,
        indicator_code,
        indicator_name,
        year,
        value,
        source_url,
        fetched_at
    from {{ source('world_bank', 'world_bank_indicators') }}

),

cleaned as (

    select
        upper(trim(country_code)) as country_code,
        trim(country_name) as country_name,
        trim(indicator_code) as indicator_code,
        trim(indicator_name) as indicator_name,
        year,
        value,
        source_url,
        fetched_at
    from source_data
    where country_code is not null
      and indicator_code is not null
      and year is not null

)

select *
from cleaned
