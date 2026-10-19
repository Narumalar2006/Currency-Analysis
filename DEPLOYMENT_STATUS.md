# Deployment and verification status

This repository contains the initial Currency Analysis pipeline source code and deployment configuration.

## Included
- Docker Compose services for PostgreSQL, Apache Airflow, and Metabase.
- A custom Airflow image that installs the Python requirements.
- PostgreSQL schema initialization.
- Example SQL queries for dashboard charts and summary statistics.
- The Airflow DAG under `dags/`.

## Not yet verified
- Docker Desktop successfully starting on the target Windows computer.
- Airflow DAG completing successfully against the live Frankfurter API.
- Currency rows appearing in PostgreSQL after a DAG run.
- Metabase being connected to PostgreSQL and a dashboard being saved.

Do not describe the project as end-to-end tested until these checks pass.

## Start locally
1. Ensure Docker Desktop is running.
2. From the project root, run `docker compose up --build -d`.
3. Wait for the services to start.
4. Open Airflow at http://localhost:8080 and Metabase at http://localhost:3000.
5. In Metabase, add a PostgreSQL database connection:
   - Host: `postgres`
   - Port: `5432`
   - Database: `currency_db`
   - Username: `currency_user`
   - Password: `change_this_password`
6. In Airflow, locate `currency_analysis_pipeline`, trigger it, and inspect task logs.
7. In Metabase, use the saved queries in `sql/dashboard_queries.sql` to create charts and dashboard cards.

## Important
The default credentials are for local demonstration only. Change them before any shared or production deployment. PostgreSQL initialization scripts run only when the data volume is first created; if the database volume already exists, apply schema changes manually.
