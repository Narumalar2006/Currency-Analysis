-- 1. Exchange-rate trend for one currency pair
SELECT rate_date, rate
FROM currency_rates
WHERE base_currency = 'EUR' AND quote_currency = 'INR'
ORDER BY rate_date;

-- 2. Latest rates for all quote currencies
SELECT DISTINCT ON (quote_currency)
       quote_currency, rate_date, rate
FROM currency_rates
WHERE base_currency = 'EUR'
ORDER BY quote_currency, rate_date DESC;

-- 3. Daily percentage change for EUR/INR
WITH daily AS (
  SELECT rate_date, rate,
         LAG(rate) OVER (ORDER BY rate_date) AS previous_rate
  FROM currency_rates
  WHERE base_currency = 'EUR' AND quote_currency = 'INR'
)
SELECT rate_date, rate,
       ROUND(((rate - previous_rate) / NULLIF(previous_rate, 0) * 100)::numeric, 4)
         AS daily_change_percent
FROM daily
ORDER BY rate_date;

-- 4. Minimum and maximum observed rates per currency
SELECT quote_currency, MIN(rate) AS minimum_rate, MAX(rate) AS maximum_rate
FROM currency_rates
WHERE base_currency = 'EUR'
GROUP BY quote_currency
ORDER BY quote_currency;

-- 5. 7-observation moving average for EUR/INR
SELECT rate_date, rate,
       AVG(rate) OVER (ORDER BY rate_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
         AS moving_average_7
FROM currency_rates
WHERE base_currency = 'EUR' AND quote_currency = 'INR'
ORDER BY rate_date;
