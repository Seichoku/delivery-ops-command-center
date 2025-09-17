
  
    
    

    create  table
      "delivery_ops"."main"."features__dbt_tmp"
  
    as (
      with base as (
  select
    pickup_ts,
    date_trunc('hour', pickup_ts) as pickup_hour,
    extract(hour from pickup_ts) as pickup_hour_of_day,
    pu_loc,
    do_loc,
    trip_distance_mi,
    passenger_count,
    fare_amount,
    total_amount,
    duration_min,
    case
      when trip_distance_mi <= 0.5 then 8.0
      when trip_distance_mi <= 2.0 then 20.0
      when trip_distance_mi <= 5.0 then 40.0
      else 90.0
    end as expected_duration_min
  from "delivery_ops"."main"."trips_staging"
),
labeled as (
  select
    *,
    case when duration_min > expected_duration_min then 1 else 0 end as is_late
  from base
)
select * from labeled
    );
  
  