import duckdb
import joblib
from sklearn.linear_model import LogisticRegression

con = duckdb.connect("data/delivery_ops.duckdb")
df = con.execute("SELECT late_rate, avg_dist FROM main.features").df()

X = df[["avg_dist"]]
y = (df["late_rate"] > 0).astype(int)  # late vs not late

model = LogisticRegression()
model.fit(X, y)

joblib.dump(model, "models/baseline.pkl")
print("✅ Model trained and saved to models/baseline.pkl")
