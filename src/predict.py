import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import pandas as pd
import numpy as np
import joblib
from features import add_features

bundle = joblib.load("src/model.pkl")
model, FEATURES = bundle["model"], bundle["features"]

test = pd.read_csv("data/test.csv", parse_dates=["datetime"])
t = add_features(test)
pred_log = model.predict(t[FEATURES])
pred = np.expm1(pred_log).clip(min=0)

out = pd.DataFrame({"datetime": test["datetime"], "count": pred.round().astype(int)})
out.to_csv("data/submission.csv", index=False)
print(f"wrote data/submission.csv {out.shape}")
print(out.head().to_string(index=False))
