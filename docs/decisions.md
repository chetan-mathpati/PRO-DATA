# PRO DATA — Engineering Decisions

## PostgreSQL

Used as the analytical warehouse for relational storage and analytical SQL.

## dbt

Used to separate staging, intermediate transformations, and analytical marts.

## Country-Year Grain

The integrated analytical model uses one country × one year.

## Missing Values

Source missing values remain NULL rather than being converted to zero.

## ML Validation

A chronological split is used instead of a random split because the target
represents a future-year outcome.

## Tableau

Tableau consumes curated analytical datasets rather than raw API responses.
