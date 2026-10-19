from datetime import datetime, timedelta
import requests

from airflow.sdk import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook

API_URL = "https://api.frankfurter.dev/v2/rates"
CURRENCIES = ["USD", "INR", "GBP", "JPY", "CHF", "AUD", "CAD"]
POSTGRES_CONN_ID = "currency_postgres"


@dag(
    dag_id="currency_analysis_pipeline",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["currency", "frankfurter", "postgres", "metabase"],
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
)
def currency_analysis_pipeline():

    @task
    def create_table():
        hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        hook.run("""
        CREATE TABLE IF NOT EXISTS currency_rates (
            id BIGSERIAL PRIMARY KEY,
            rate_date DATE NOT NULL,
            base_currency VARCHAR(3) NOT NULL,
            quote_currency VARCHAR(3) NOT NULL,
            rate NUMERIC(18,8) NOT NULL,
            collected_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(rate_date, base_currency, quote_currency)
        );
        CREATE INDEX IF NOT EXISTS idx_currency_rates_date
        ON currency_rates(rate_date);
        CREATE INDEX IF NOT EXISTS idx_currency_rates_pair
        ON currency_rates(base_currency, quote_currency);
        """)

    @task
    def extract():
        # Pull a rolling 90-day window so the dashboard has enough history
        # for moving averages and volatility on the first successful run.
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=90)

        params = {
            "from": start_date.isoformat(),
            "to": end_date.isoformat(),
            "base": "EUR",
            "symbols": ",".join(CURRENCIES),
        }

        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, list) or not data:
            raise ValueError("Frankfurter API returned no rate records.")

        return data

    @task
    def validate_transform(records):
        cleaned = []

        for row in records:
            date = row.get("date")
            base = row.get("base")
            quote = row.get("quote")
            rate = row.get("rate")

            if not date or base != "EUR" or quote not in CURRENCIES:
                continue

            try:
                rate = float(rate)
            except (TypeError, ValueError):
                continue

            if rate <= 0:
                continue

            cleaned.append((date, base, quote, rate))

        if not cleaned:
            raise ValueError("No valid exchange-rate records after validation.")

        return cleaned

    @task
    def load(records):
        hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

        sql = """
        INSERT INTO currency_rates
            (rate_date, base_currency, quote_currency, rate)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (rate_date, base_currency, quote_currency)
        DO UPDATE SET
            rate = EXCLUDED.rate,
            collected_at = CURRENT_TIMESTAMP;
        """

        hook.insert_rows(
            table="currency_rates",
            rows=records,
            target_fields=["rate_date", "base_currency", "quote_currency", "rate"],
            commit_every=500,
        )

    table = create_table()
    raw = extract()
    clean = validate_transform(raw)
    table >> raw >> clean >> load(clean)


currency_analysis_pipeline()
