PRO DATA

GLOBAL ECONOMIC, ENERGY & SUPPLY-CHAIN INTELLIGENCE PLATFORM

See the forces shaping the global economy.

PRO DATA is an end-to-end data intelligence platform that combines
World Bank economic indicators with EIA international petroleum
and liquids data to analyze economic trends, energy signals and
country-level relationships.

ARCHITECTURE

Public APIs
    ↓
Python ingestion
    ↓
PostgreSQL raw layer
    ↓
dbt staging → intermediate → analytical marts
    ↓
SQL analytics / ML / Tableau

DATA

World Bank
- GDP
- GDP growth
- GDP per capita
- inflation
- unemployment
- trade
- exports
- imports

EIA
- petroleum production
- crude oil production
- petroleum consumption

The integrated analytical grain is one country x one year.

ANALYTICS

The SQL layer covers:

- country benchmarking
- growth acceleration
- economic and inflation regimes
- energy dependency signals
- economic-energy divergence

ML

Experimental classification baseline for identifying whether
petroleum production declines by at least 10% in the following year.

Uses chronological validation, preprocessing pipelines,
logistic regression, class balancing and ROC-AUC evaluation.

The model is an analytical baseline, not a production forecasting
service.

TABLEAU

Interactive dashboards covering:

- global economic and energy trends
- country intelligence
- energy risk signals
- country benchmarking

VALIDATION

- 137,280 World Bank records
- 16,887 EIA records
- 17,160 integrated country-year records
- 260 countries
- 8 economic indicators
- 66 periods
- 0 duplicate country-year records
- 9 dbt models
- 33 dbt tests
- 42/42 dbt checks passing

TECH STACK

Python | PostgreSQL | SQL | dbt | pandas | scikit-learn |
Tableau | Git/GitHub

REPOSITORY

analytics/       SQL analytics and Tableau datasets
dashboard/       Tableau workbook
dbt/             transformation models
docs/             architecture and methodology
ingestion/        source ingestion
ml/               feature engineering and modeling
tests/            validation
warehouse/        PostgreSQL schemas and migrations

DOCUMENTATION

docs/architecture.md
docs/data_dictionary.md
docs/methodology.md
docs/decisions.md
docs/tableau_setup.md
docs/ml_setup.md

LIMITATIONS

Source coverage varies across countries and years.

Missing source observations remain NULL rather than being treated
as zero.

Analytical relationships are descriptive and do not establish
causation.

LICENSE

MIT