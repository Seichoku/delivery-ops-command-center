# TODO: implement NYC TLC data download and land to DuckDB
# src/etl/ingest.py
import duckdb
import pandas as pd
from pathlib import Path

import requests, certifi

DATA_DIR = Path("data")
DB_PATH = DATA_DIR / "delivery_ops.duckdb"
TABLE = "raw_trips"

# NYC TLC yellow trips (Jan 2023)
URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"

LOCAL_PARQUET = DATA_DIR / "yellow_tripdata_2023-01.parquet"

def download_parquet():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if LOCAL_PARQUET.exists():
        return
    with requests.get(URL, stream=True, verify=certifi.where()) as r:
        r.raise_for_status()
        with open(LOCAL_PARQUET, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

def main():
    download_parquet()

    # Read parquet into DataFrame (column-subset to keep it light)
    cols = [
        "tpep_pickup_datetime","tpep_dropoff_datetime",
        "passenger_count","trip_distance","PULocationID","DOLocationID",
        "fare_amount","total_amount","payment_type","congestion_surcharge"
    ]
    df = pd.read_parquet(LOCAL_PARQUET, columns=cols)

    # Basic cleaning
    df = df.dropna(subset=["tpep_pickup_datetime","tpep_dropoff_datetime","trip_distance"])
    df = df[df["trip_distance"] >= 0]
    df["duration_min"] = (
        (pd.to_datetime(df["tpep_dropoff_datetime"]) - pd.to_datetime(df["tpep_pickup_datetime"]))
        .dt.total_seconds() / 60.0
    )
    df = df[(df["duration_min"] >= 0) & (df["duration_min"] <= 240)]  # clamp to 4h

    con = duckdb.connect(DB_PATH.as_posix())
    con.execute(f"CREATE SCHEMA IF NOT EXISTS raw;")
    con.execute(f"DROP TABLE IF EXISTS raw.{TABLE};")
    con.register("df", df)
    con.execute(f"CREATE TABLE raw.{TABLE} AS SELECT * FROM df;")
    con.close()

    print(f"Loaded {len(df):,} rows into {DB_PATH} as raw.{TABLE}")

if __name__ == "__main__":
    main()
