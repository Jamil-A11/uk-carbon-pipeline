WITH fuels AS (
    SELECT
        from_ts,
        to_ts,
        region_id,
        region_name,
        is_aggregate,
        unnest(generation_mix) AS g
    FROM {{ ref('silver_regional_intensity') }}
)

SELECT
    from_ts,
    to_ts,
    region_id,
    region_name,
    is_aggregate,
    g.fuel AS fuel,
    g.perc AS generation_pct
FROM fuels