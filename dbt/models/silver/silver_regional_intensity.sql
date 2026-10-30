WITH cleaned AS (
    SELECT
        strptime(from_ts, '%Y-%m-%dT%H:%MZ') AS from_ts,
        strptime(to_ts, '%Y-%m-%dT%H:%MZ') AS to_ts,
        region_id,
        region_name,
        forecast AS forecast_gco2,
        intensity_index,
        generation_mix,
        CASE
            WHEN region_id >= 15 THEN true
            ELSE false
        END AS is_aggregate
    FROM {{ source('bronze', 'bronze_regional_intensity') }}
),

ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY region_id, from_ts
            ORDER BY forecast_gco2
        ) AS row_num
    FROM cleaned
)

SELECT * EXCLUDE (row_num)
FROM ranked
WHERE row_num = 1
    AND from_ts >= TIMESTAMP '2026-09-01 00:00:00'
    AND from_ts < TIMESTAMP '2026-10-01 00:00:00'