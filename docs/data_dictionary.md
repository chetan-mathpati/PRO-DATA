PRO DATA - DATA DICTIONARY

Grain: one country x one year


IDENTIFIERS

country_code
Country identifier.

country_name
Country name.

year
Observation year.


ECONOMIC FIELDS

gdp_usd
GDP in current US dollars.

gdp_growth_pct
Annual GDP growth percentage.

gdp_per_capita_usd
GDP per capita in current US dollars.

inflation_pct
Consumer price inflation.

unemployment_pct
Unemployment percentage of the labor force.

trade_pct_gdp
Trade as a percentage of GDP.

exports_pct_gdp
Exports of goods and services as a percentage of GDP.

imports_pct_gdp
Imports of goods and services as a percentage of GDP.


ENERGY FIELDS

total_petroleum_production_tbpd
Total petroleum and other liquids production.

crude_oil_production_tbpd
Crude oil including lease condensate production.

petroleum_consumption_tj
Petroleum and other liquids consumption.

previous_petroleum_production_tbpd
Previous-year total petroleum production.

previous_crude_oil_production_tbpd
Previous-year crude oil production.

petroleum_production_yoy_pct
Year-over-year change in petroleum production.

crude_oil_production_yoy_pct
Year-over-year change in crude oil production.

crude_share_of_petroleum_production_pct
Crude oil production as a percentage of total petroleum production.


ROLLING METRICS

gdp_growth_5yr_avg
Five-year rolling average of GDP growth.

inflation_5yr_avg
Five-year rolling average of inflation.

petroleum_production_5yr_avg
Five-year rolling average of petroleum production.


MISSING VALUES

Source-level missing observations are stored as NULL.

NULL is not interpreted as zero.

Missing observations are retained where source coverage is incomplete.