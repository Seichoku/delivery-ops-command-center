# expectations/bootstrap_check.py
from great_expectations.dataset import PandasDataset
import duckdb

con = duckdb.connect("data/delivery_ops.duckdb")
df = con.execute("select * from main.features limit 5000").fetchdf()

ds = PandasDataset(df)
ds.expect_column_values_to_not_be_null("pickup_ts")
ds.expect_column_values_to_be_between("trip_distance_mi", min_value=0, max_value=100)
ds.expect_column_values_to_be_between("duration_min", min_value=0, max_value=240)

results = ds.validate()
print("Success:", results["success"])
for r in results["results"]:
    print(r["expectation_config"]["expectation_type"], "->", r["success"])
