PRO DATA - TABLEAU SETUP

PURPOSE

The Tableau workbook uses curated CSV datasets generated
from the PostgreSQL analytical mart.

DATASETS

analytics/exports/global_economic_energy.csv
Main country-year analytical dataset.

analytics/exports/country_benchmark.csv
Latest-year country comparison dataset.

analytics/exports/energy_signals.csv
Recent energy signal dataset.


WORKBOOK

dashboard/PRO_DATA_Intelligence.twb

The workbook is configured against the local repository
data-export path used during development.

When opening the workbook on another machine, reconnect
the Tableau data source to the local:

analytics/exports/

directory in the cloned repository.


REGENERATING DATASETS

The CSV datasets can be regenerated with:

python analytics/export_tableau_datasets.py

The command reads from the PostgreSQL analytical mart
and recreates the Tableau-ready exports.


RECOMMENDED WORKFLOW

1. Start the PostgreSQL environment.
2. Run the ingestion pipeline if source data needs refreshing.
3. Run dbt build.
4. Run the Tableau export script.
5. Open dashboard/PRO_DATA_Intelligence.twb.
6. Reconnect the data source if Tableau reports a local path mismatch.