with src as (
  select
    CAST(tpep_pickup_datetime AS TIMESTAMP)   as pickup_ts,
    CAST(tpep_dropoff_datetime AS TIMESTAMP)  as dropoff_ts,
    CAST(passenger_count AS INTEGER)          as passenger_count,
    CAST(trip_distance AS DOUBLE)             as trip_distance_mi,
    CAST(PULocationID AS INTEGER)             as pu_loc,
    CAST(DOLocationID AS INTEGER)             as do_loc,
    CAST(fare_amount AS DOUBLE)               as fare_amount,
    CAST(total_amount AS DOUBLE)              as total_amount,
    CAST(payment_type AS INTEGER)             as payment_type,
    CAST(congestion_surcharge AS DOUBLE)      as congestion_surcharge,
    CAST(duration_min AS DOUBLE)              as duration_min
  from raw.raw_trips
  where
    -- keep the month we actually ingested
    pickup_ts >= TIMESTAMP '2023-01-01'
    and pickup_ts <  TIMESTAMP '2023-02-01'
    -- drop zero/negative distances
    and trip_distance_mi > 0
    -- keep reasonable durations
    and duration_min between 0 and 240
)
select * from src