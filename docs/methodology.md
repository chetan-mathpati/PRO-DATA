# PRO DATA — Methodology

## Purpose

PRO DATA combines economic indicators from the World Bank with international
petroleum and liquids data from the U.S. Energy Information Administration.

The objective is to create an analytical system that connects:

- economic growth
- inflation
- unemployment
- trade
- petroleum production
- crude oil production
- petroleum consumption

## Data grain

The integrated analytical grain is:

**one country × one year**

## Pipeline

External APIs
→ raw PostgreSQL tables
→ dbt staging
→ dbt intermediate transformations
→ analytical marts
→ SQL analytics
→ ML features
→ Tableau datasets

## Data quality

The pipeline uses:

- not-null tests
- uniqueness tests
- source validation
- duplicate checks
- explicit normalization of missing source values
- deterministic transformations
- idempotent World Bank loading
- time-aware ML validation

## ML methodology

The model predicts whether petroleum production will decline by at least
10% in the following year.

The target is constructed from the following year's observed production.

The train/test split is chronological rather than random to reduce
temporal leakage.

The current model is intended as an analytical demonstration rather than
a production forecasting service.

## Interpretation

Correlation between economic and energy variables does not establish
causation.

Missing observations are retained where source coverage is incomplete
rather than artificially filled without methodological justification.