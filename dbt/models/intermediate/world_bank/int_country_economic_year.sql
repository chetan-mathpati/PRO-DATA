with annual_data as (

    select
        country_code,
        country_name,
        year,

        max(case when indicator_code = 'NY.GDP.MKTP.CD'
            then value end) as gdp_usd,

        max(case when indicator_code = 'NY.GDP.MKTP.KD.ZG'
            then value end) as gdp_growth_pct,

        max(case when indicator_code = 'NY.GDP.PCAP.CD'
            then value end) as gdp_per_capita_usd,

        max(case when indicator_code = 'FP.CPI.TOTL.ZG'
            then value end) as inflation_pct,

        max(case when indicator_code = 'SL.UEM.TOTL.ZS'
            then value end) as unemployment_pct,

        max(case when indicator_code = 'NE.TRD.GNFS.ZS'
            then value end) as trade_pct_gdp,

        max(case when indicator_code = 'NE.EXP.GNFS.ZS'
            then value end) as exports_pct_gdp,

        max(case when indicator_code = 'NE.IMP.GNFS.ZS'
            then value end) as imports_pct_gdp

    from {{ ref('stg_world_bank_indicators') }}

    group by
        country_code,
        country_name,
        year

)

select
    country_code,
    country_name,
    year,
    gdp_usd,
    gdp_growth_pct,
    gdp_per_capita_usd,
    inflation_pct,
    unemployment_pct,
    trade_pct_gdp,
    exports_pct_gdp,
    imports_pct_gdp
from annual_data
