# PRO DATA - Architecture

## System Overview

PRO DATA is an end-to-end analytical platform that integrates macroeconomic indicators from the World Bank with international petroleum and liquids data from the U.S. Energy Information Administration (EIA).

```text
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
