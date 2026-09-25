import pandas as pd
import numpy as np

FEATURES = ["season", "holiday", "workingday", "weather", "temp", "atemp",
            "humidity", "windspeed",
            "hour", "dow", "month", "year",
            "hour_sin", "hour_cos", "month_sin", "month_cos"]

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["datetime"] = pd.to_datetime(d["datetime"])
    d["hour"] = d["datetime"].dt.hour
    d["dow"] = d["datetime"].dt.dayofweek
    d["month"] = d["datetime"].dt.month
    d["year"] = d["datetime"].dt.year
    d["hour_sin"] = np.sin(2 * np.pi * d["hour"] / 24)
    d["hour_cos"] = np.cos(2 * np.pi * d["hour"] / 24)
    d["month_sin"] = np.sin(2 * np.pi * (d["month"] - 1) / 12)
    d["month_cos"] = np.cos(2 * np.pi * (d["month"] - 1) / 12)
    return d
