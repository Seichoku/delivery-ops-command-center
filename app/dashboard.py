import streamlit as st
import duckdb
from pathlib import Path

st.set_page_config(page_title="Delivery Ops Command Center", layout="wide")
st.title("Delivery Ops Command Center")
st.caption("Live metrics powered by DuckDB + dbt models (main.features)")

DB_PATH = Path("data") / "delivery_ops.duckdb"


@st.cache_data(show_spinner=False)
def load_features():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"DuckDB not found at {DB_PATH}. "
            "Run: `python src/etl/ingest.py` then `dbt run --project-dir dbt`."
        )
    con = duckdb.connect(DB_PATH.as_posix(), read_only=True)
    # Aggregate once for KPIs and chart
    df_hourly = con.execute(
        """
        with h as (
          select
            pickup_hour,
            avg(is_late)::DOUBLE as late_rate,
            avg(trip_distance_mi)::DOUBLE as avg_dist,
            avg(duration_min)::DOUBLE as avg_duration_min,
            count(*)::BIGINT as trips
          from main.features
          group by 1
        )
        select * from h order by pickup_hour
    """
    ).fetchdf()

    # Global KPIs
    kpis = (
        con.execute(
            """
        select
          round(avg(1 - is_late)::numeric, 4) as on_time_rate,
          round(avg(duration_min)::numeric, 2) as avg_duration_min,
          count(*)::BIGINT as total_trips
        from main.features
    """
        )
        .fetchdf()
        .iloc[0]
        .to_dict()
    )

    con.close()
    return df_hourly, kpis


try:
    df_hourly, kpis = load_features()
except Exception as e:
    st.error(str(e))
    st.stop()

# ===== KPIs =====
col1, col2, col3 = st.columns(3)
col1.metric("On-time %", f"{kpis['on_time_rate'] * 100:.1f}%")
col2.metric("Avg Duration (min)", f"{kpis['avg_duration_min']:.2f}")
col3.metric("Total Trips", f"{int(kpis['total_trips']):,}")

st.divider()

# ===== Charts =====
left, right = st.columns((2, 1))

with left:
    st.subheader("Late Rate by Hour")
    # Guard against empty df
    if not df_hourly.empty:
        # Streamlit wants datetime index for time-series
        plot_df = df_hourly.set_index("pickup_hour")[["late_rate"]]
        st.line_chart(plot_df)
    else:
        st.info("No hourly data available.")

with right:
    st.subheader("Distance & Trips (by hour)")
    if not df_hourly.empty:
        st.bar_chart(df_hourly.set_index("pickup_hour")[["avg_dist"]])
        st.caption("Bars show avg trip distance (mi).")
    else:
        st.info("No distance data available.")

st.divider()

# ===== Sample table (peek) =====
st.subheader("Hourly Aggregates (preview)")
st.dataframe(df_hourly.head(50), use_container_width=True, hide_index=True)
