SELECT DISTINCT
    region_id,
    region_name,
    is_aggregate
FROM {{ ref('silver_regional_intensity') }}
ORDER BY region_id