PRO DATA - ARCHITECTURE

SYSTEM OVERVIEW

PRO DATA is an end-to-end analytical platform that integrates
macroeconomic indicators from the World Bank with international
petroleum and liquids data from the U.S. Energy Information
Administration (EIA).


DATA FLOW

World Bank API ----\
                    +--> Python ingestion --> PostgreSQL raw
EIA API -----------/                              |
                                                   v
                                             dbt staging
                                                   |
                                                   v
                                          dbt intermediate
                                                   |
                                                   v
                                           Analytical marts
                                          /        |        \
                                         v         v         v
                                   SQL Analytics   ML     Tableau
                                                     |
                                                     v
                                                 Evaluation


CORE TECHNOLOGY

Python
PostgreSQL
SQL
dbt
pandas
scikit-learn
Tableau
Git/GitHub


ANALYTICAL GRAIN

The integrated analytical model uses:

one country x one year

Source datasets have different structures and coverage periods.
They are normalized before being integrated into the country-year
analytical model.


DESIGN PRINCIPLES

1. Preserve source data in raw storage.
2. Keep transformations reproducible.
3. Use an explicit analytical grain.
4. Test data quality before analysis.
5. Use chronological validation for ML.
6. Keep Tableau dependent on curated analytical data.


DATA LAYERS

RAW

Stores source observations from external APIs with source metadata
and original source payloads where applicable.

STAGING

Standardizes source structures and data types for downstream
transformations.

INTERMEDIATE

Combines and transforms source datasets into reusable analytical
structures.

MARTS

Provides curated analytical datasets at the defined country-year
grain.


ANALYTICS OUTPUTS

SQL Analytics
Analytical queries for economic and energy relationships.

ML
Feature engineering and an experimental petroleum production
decline classification baseline.

Tableau
Interactive dashboards built from curated analytical datasets.


REPRODUCIBILITY

Source ingestion, transformations, analytical logic and ML
processing are maintained as version-controlled project code.

Credentials, local environments, generated artifacts and runtime
logs are excluded from version control where appropriate.