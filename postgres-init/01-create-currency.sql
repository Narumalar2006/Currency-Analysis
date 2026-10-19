CREATE TABLE IF NOT EXISTS currency_rates (
    id BIGSERIAL PRIMARY KEY,
    rate_date DATE NOT NULL,
    base_currency VARCHAR(3) NOT NULL,
    quote_currency VARCHAR(3) NOT NULL,
    rate NUMERIC(18,8) NOT NULL CHECK (rate > 0),
    collected_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (rate_date, base_currency, quote_currency)
);

CREATE INDEX IF NOT EXISTS idx_currency_rates_date
    ON currency_rates(rate_date);

CREATE INDEX IF NOT EXISTS idx_currency_rates_pair
    ON currency_rates(base_currency, quote_currency);
