# PRO DATA — Architecture

World Bank API + EIA API
        ↓
Python ingestion
        ↓
PostgreSQL raw layer
        ↓
dbt staging
        ↓
dbt intermediate models
        ↓
Analytical marts
        ↓
 ┌───────────────┬───────────────┐
 ↓               ↓               ↓
SQL Analytics   ML Features    Tableau
                    ↓
                ML Model
                    ↓
                Evaluation

## Core Technology

- Python
- PostgreSQL
- SQL
- dbt
- pandas
- scikit-learn
- Tableau
- Git/GitHub

## Analytical Grain

One country × one year.

## Design Principles

1. Preserve source data in raw storage.
2. Keep transformations reproducible.
3. Use explicit analytical grain.
4. Test data quality before analysis.
5. Use chronological validation for ML.
6. Keep Tableau dependent on curated analytical data.
