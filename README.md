# Currency Analysis — Apache Airflow + PostgreSQL + Metabase

Pipeline:
Frankfurter API → Airflow → validation/transformation → PostgreSQL → Metabase

## Dashboard requirements
- Exchange-rate trend line charts
- Currency comparison charts
- Daily change indicators
- Monthly/yearly trends
- Minimum/maximum rate statistics
- Moving-average charts
- Volatility analysis
- Currency-pair filters
- Date-range filters
- Summary KPI cards

## First setup
1. Install Docker Desktop and make sure Docker is running.
2. Download the official Airflow Docker Compose file into this folder:
   https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml
3. Create folders: dags, logs, plugins, config.
4. Put `currency_analysis_dag.py` inside `dags/`.
5. If the official Airflow image does not already contain the Postgres provider, use the included `requirements.txt` with a custom Airflow image; for the demo quick-start, the provider is commonly already available.
6. Start Airflow with Docker Compose. The included override mounts `postgres-init`, which creates the `currency` database on a fresh PostgreSQL volume.
7. Create an Airflow Postgres connection named `currency_postgres`.
8. Point it to the Postgres service used by Airflow.
9. Create a database named `currency` (or use the Airflow database if preferred).
10. Trigger `currency_analysis_pipeline`.
11. Connect Metabase to the PostgreSQL database and build the dashboard.

## Suggested connection
Connection ID: currency_postgres
Type: Postgres
Host: postgres
Port: 5432
Database: currency
Login: airflow
Password: airflow

Note: if you create a separate `currency` database, create it first in PostgreSQL.
