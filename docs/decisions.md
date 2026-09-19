PRO DATA - ENGINEERING DECISIONS

POSTGRESQL

PostgreSQL is used as the warehouse for raw source data, transformed models and analytical queries.

Keeping the data in a relational warehouse provides a consistent SQL interface across ingestion, transformation and analysis.


PYTHON INGESTION

Python is used for external API ingestion.

The ingestion layer handles:
- API requests
- response normalization
- missing-value normalization
- database loading
- source metadata preservation


DBT

dbt separates transformation logic into staging, intermediate and analytical marts.

This keeps transformation logic version controlled and testable.


COUNTRY-YEAR GRAIN

The integrated analytical model uses:

one country x one year

This provides a common analytical grain across the economic and energy datasets.


MISSING VALUES

Source missing values remain NULL.

A missing observation is not automatically treated as zero.

This prevents unavailable source data from being interpreted as an observed zero value.


ML VALIDATION

The ML target represents a future-year outcome.

A chronological train/test split is therefore used instead of a random split.

This reduces the risk of temporal leakage during evaluation.


TABLEAU

Tableau consumes curated analytical datasets rather than raw API responses.

This separates the BI layer from source ingestion and warehouse implementation.


EXPERIMENTAL ML

The current ML component is treated as an experimental analytical baseline.

It is not presented as a production forecasting service.


REPRODUCIBILITY

The root requirements.txt defines the project direct Python dependencies.

Credentials, virtual environments, runtime logs and generated ML artifacts are excluded from version control where appropriate.
