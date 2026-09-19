with indicators as (

    select
        indicator_code,
        max(indicator_name) as indicator_name
    from {{ ref('stg_world_bank_indicators') }}
    where indicator_code is not null
    group by indicator_code

)

select
    row_number() over (order by indicator_code) as indicator_key,
    indicator_code,
    indicator_name,
    case
        when indicator_code like 'NY.%' then 'economy'
        when indicator_code like 'FP.%' then 'prices'
        when indicator_code like 'SL.%' then 'labor'
        when indicator_code like 'NE.%' then 'trade'
        else 'other'
    end as domain
from indicators
