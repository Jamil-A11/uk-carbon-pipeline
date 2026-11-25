SELECT
    from_ts,
    forecast_gco2,
    actual_gco2,
    actual_gco2 - forecast_gco2 AS forecast_error_gco2,
    intensity_index
FROM {{ ref('silver_national_intensity') }}
