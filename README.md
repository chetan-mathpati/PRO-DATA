# PRO DATA

### Global Economic, Energy & Supply-Chain Intelligence Platform

> See the forces shaping the global economy.

PRO DATA is an end-to-end data analytics platform integrating macroeconomic indicators with global energy production and consumption data.

## Architecture

Public Data Sources -> Python Ingestion -> PostgreSQL -> dbt -> Analytics Marts -> SQL / ML / Tableau

## Core capabilities

- Economic and energy trend analysis
- Country benchmarking
- Energy dependency signals
- Economic-energy divergence analysis
- Experimental ML baseline
- Interactive Tableau intelligence dashboards

## Validation

- 137,280 World Bank records
- 16,887 EIA records
- 17,160 integrated mart records
- 260 countries
- 8 indicators
- 66 periods
- 0 duplicate country-year records
- dbt: 9 models, 33 tests, 42/42 passing

## Repository

- analytics/ — analytical SQL and Tableau exports
- dashboard/ — Tableau workbook
- dbt/ — transformation layer
- docs/ — architecture and methodology
- ingestion/ — source ingestion pipelines
- ml/ — feature engineering and experimental modeling
- tests/ — validation
- warehouse/ — PostgreSQL infrastructure

