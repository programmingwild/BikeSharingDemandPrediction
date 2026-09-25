import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from features import add_features, FEATURES

train = pd.read_csv("data/train.csv", parse_dates=["datetime"])
train = add_features(train)
X = train[FEATURES]
y = np.log1p(train["count"])

Xtr, Xv, ytr, yv = train_test_split(X, y, test_size=0.2, shuffle=False)

def rmsle(y_true_log, y_pred_log):
    return float(np.sqrt(mean_squared_error(y_true_log, y_pred_log)))

models = {
    "xgb": XGBRegressor(n_estimators=500, max_depth=7, learning_rate=0.05,
                        subsample=0.8, colsample_bytree=0.8,
                        random_state=42, n_jobs=-1),
    "hgb": HistGradientBoostingRegressor(max_iter=500, max_depth=7,
                                         learning_rate=0.05, random_state=42),
}
best_name, best_score, best_model = None, 1e9, None
for name, m in models.items():
    m.fit(Xtr, ytr)
    s = rmsle(yv, m.predict(Xv))
    print(f"{name}: RMSLE={s:.4f}")
    if s < best_score:
        best_name, best_score, best_model = name, s, m

print(f"BEST: {best_name} RMSLE={best_score:.4f}")

# Retrain best on full data
best_model.fit(X, y)
joblib.dump({"model": best_model, "features": FEATURES}, "src/model.pkl")
print("saved src/model.pkl")

# Feature importance
try:
    imp = pd.Series(best_model.feature_importances_, index=FEATURES).sort_values(ascending=False)
    print(imp.to_string())
except AttributeError:
    from sklearn.inspection import permutation_importance
    r = permutation_importance(best_model, Xv, yv, n_repeats=5, random_state=42, n_jobs=-1)
    imp = pd.Series(r.importances_mean, index=FEATURES).sort_values(ascending=False)
    print(imp.to_string())
