with source_data as (

    select
        country_code,
        country_name,
        product_id,
        product_name,
        activity_id,
        activity_name,
        period,
        value,
        unit,
        source_url,
        fetched_at
    from {{ source('eia', 'eia_energy') }}

),

cleaned as (

    select
        upper(trim(country_code)) as country_code,
        trim(country_name) as country_name,
        trim(product_id) as product_id,
        trim(product_name) as product_name,
        trim(activity_id) as activity_id,
        trim(activity_name) as activity_name,
        period,
        value,
        trim(unit) as unit,
        source_url,
        fetched_at
    from source_data
    where country_code is not null
      and product_id is not null
      and activity_id is not null
      and period is not null

)

select *
from cleaned
