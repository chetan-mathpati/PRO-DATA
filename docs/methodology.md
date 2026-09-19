PRO DATA - METHODOLOGY

PURPOSE

PRO DATA combines economic indicators from the World Bank with
international petroleum and liquids data from the U.S. Energy
Information Administration.

The analytical system connects:

- economic growth
- inflation
- unemployment
- trade
- petroleum production
- crude oil production
- petroleum consumption


DATA GRAIN

The integrated analytical grain is:

one country x one year

Source datasets have different structures and coverage periods.
Observations are normalized before being integrated into the
country-year analytical model.


PIPELINE

External APIs
    |
    v
Python ingestion
    |
    v
PostgreSQL raw tables
    |
    v
dbt staging
    |
    v
dbt intermediate transformations
    |
    v
Analytical marts
    |
    +---- SQL analytics
    |
    +---- ML features
    |
    +---- Tableau datasets


INGESTION

WORLD BANK

The World Bank ingestion layer retrieves the configured economic
indicators and stores source observations in PostgreSQL.

The business key is:

country + indicator + year

Source metadata is preserved with the raw observation.


EIA

The EIA ingestion layer retrieves annual petroleum production
and consumption observations for the configured product and
activity combinations.

Source representations such as --, empty values and equivalent
missing-value markers are normalized to database NULL.


DATA QUALITY

The pipeline applies:

- source validation
- primary-key constraints
- uniqueness tests
- not-null tests where appropriate
- duplicate checks
- missing-value normalization
- dbt model tests
- integrated-grain validation
- database validation scripts

Transformations are deterministic and version controlled.


ANALYTICAL TRANSFORMATIONS

The integrated mart combines economic and energy observations
at country-year grain.

Derived metrics include:

- year-over-year production changes
- five-year rolling averages
- crude production share
- previous-year production values

Derived metrics use available observations and do not treat
missing source values as zero.


ML METHODOLOGY

The experimental model predicts whether petroleum production
will decline by at least 10 percent in the following year.

The target is constructed from the following year's observed
petroleum production.

The train/test split is chronological rather than random because
the target represents a future-year outcome.

The current model is an analytical demonstration, not a
production forecasting service.


INTERPRETATION

Relationships between economic and energy variables are
descriptive associations. They do not establish causation.

Incomplete source coverage is retained where possible rather
than being artificially imputed without a documented reason.