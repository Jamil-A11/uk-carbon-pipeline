WITH times AS (
    SELECT
        from_ts,
        (from_ts AT TIME ZONE 'UTC') AT TIME ZONE 'Europe/London' AS from_ts_uk
    FROM {{ ref('silver_national_intensity') }}
)

SELECT
    from_ts,
    from_ts_uk,
    CAST(from_ts_uk AS DATE) AS date_uk,
    hour(from_ts) AS hour_utc,
    hour(from_ts_uk) AS hour_uk,
    dayname(from_ts_uk) AS day_name,
    isodow(from_ts_uk) >= 6 AS is_weekend
FROM times