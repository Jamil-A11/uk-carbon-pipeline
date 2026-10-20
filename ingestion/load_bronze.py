import duckdb

DB_PATH = "data/warehouse.duckdb"


def load_national(con):
    con.sql("""
        CREATE OR REPLACE TABLE bronze_national_intensity AS
        SELECT unnest(data, recursive := true)
        FROM read_json('data/bronze/intensity_daily/*.json')
    """)


def load_regional(con):
    con.sql("""
        CREATE OR REPLACE TABLE bronze_regional_intensity AS
        WITH periods AS (
            SELECT unnest(data) AS p
            FROM read_json('data/bronze/intensity_regional/*.json')
        ),
        regions AS (
            SELECT
                p."from" AS from_ts,
                p."to" AS to_ts,
                unnest(p.regions) AS r
            FROM periods
        )
        SELECT
            from_ts,
            to_ts,
            r.regionid AS region_id,
            r.shortname AS region_name,
            r.intensity.forecast AS forecast,
            r.intensity.index AS intensity_index,
            r.generationmix AS generation_mix
        FROM regions
    """)


def main():
    con = duckdb.connect(DB_PATH)
    load_national(con)
    load_regional(con)
    con.sql("SELECT COUNT(*) FROM bronze_national_intensity").show()
    con.sql("SELECT COUNT(*) FROM bronze_regional_intensity").show()


if __name__ == "__main__":
    main()