WITH cleaned AS (
    SELECT
        strptime("from", '%Y-%m-%dT%H:%MZ') AS from_ts,
        strptime("to", '%Y-%m-%dT%H:%MZ') AS to_ts,
        forecast AS forecast_gco2,
        actual AS actual_gco2,
        "index" AS intensity_index
    FROM {{ source('bronze', 'bronze_national_intensity') }}
)

SELECT *
FROM cleaned
WHERE from_ts >= TIMESTAMP '2026-09-01 00:00:00'
    AND from_ts < TIMESTAMP '2026-10-01 00:00:00'