"""BikeShare Demand Studio — premium UI backed by Streamlit.

Run locally with: streamlit run app_v2.py
The live entrypoint (streamlit_app.py) imports this module.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from src.features import add_features
import ui_v2 as v2

st.set_page_config(page_title="BikeShare · Demand Studio", page_icon="🚲",
                   layout="wide", initial_sidebar_state="collapsed")
v2.inject()

SEASONS = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
WEATHER = {1: "Clear", 2: "Mist", 3: "Light rain / snow", 4: "Heavy rain / snow"}
DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
REQUIRED_COLUMNS = ["datetime", "season", "holiday", "workingday", "weather",
                    "temp", "atemp", "humidity", "windspeed"]
PRESETS = {
    "Morning rush": dict(date="2012-06-15", hour=8, season=3, weather=1, workingday=1, t_c=20.0, hum=60, wind=10),
    "Evening rush": dict(date="2012-06-15", hour=18, season=3, weather=1, workingday=1, t_c=24.0, hum=55, wind=12),
    "Weekend midday": dict(date="2012-06-16", hour=14, season=3, weather=1, workingday=0, t_c=28.0, hum=50, wind=8),
    "Rainy commute": dict(date="2012-06-15", hour=9, season=2, weather=3, workingday=1, t_c=15.0, hum=85, wind=20),
}
DEFAULTS = dict(in_date="2012-06-15", in_hour=8, in_season=3, in_weather=1,
                in_workingday=1, in_holiday=0, in_t=22.0, in_at=24.0, in_hum=60, in_wind=12)
for k, val in DEFAULTS.items():
    st.session_state.setdefault(k, val)


def apply_preset(preset):
    """Runs before widgets are created, so keyed session values can be updated."""
    for k, val in preset.items():
        st.session_state[f"in_{k}"] = pd.to_datetime(val).date() if k == "date" else val
    st.session_state["in_at"] = preset["t_c"] + 2.0  # kept for compatibility


@st.cache_resource
def load_model():
    b = joblib.load("src/model.pkl")
    return b["model"], b["features"]


@st.cache_data
def load_train():
    return pd.read_csv("data/train.csv", parse_dates=["datetime"])


model, FEATURES = load_model()


def norm(t_c, at_c, hum, wind):
    return (t_c + 8) / 47.0, (at_c + 16) / 66.0, hum / 100.0, wind / 67.0


def row_for(date_str, hour, season, holiday, workingday, weather, temp, atemp, hum, wind):
    return add_features(pd.DataFrame([{
        "datetime": pd.to_datetime(f"{date_str} {hour:02d}:00"), "season": season,
        "holiday": holiday, "workingday": workingday, "weather": weather,
        "temp": temp, "atemp": atemp, "humidity": hum, "windspeed": wind}]))


def forecast(date_str, season, holiday, workingday, weather, temp, atemp, hum, wind):
    return [float(np.expm1(model.predict(row_for(date_str, h, season, holiday, workingday,
                                               weather, temp, atemp, hum, wind)[FEATURES])[0]))
            for h in range(24)]


def score_upload(file):
    """Validate and score an uploaded CSV, raising friendly ValueError messages."""
    raw = pd.read_csv(file)
    missing = [c for c in REQUIRED_COLUMNS if c not in raw.columns]
    if missing:
        raise ValueError("Missing columns: " + ", ".join(missing))
    raw["datetime"] = pd.to_datetime(raw["datetime"], errors="coerce")
    if raw["datetime"].isna().any():
        raise ValueError("Some datetime values could not be read.")
    if raw.empty:
        raise ValueError("The file has no rows.")
    df = add_features(raw)
    preds = np.expm1(model.predict(df[FEATURES])).clip(min=0).round().astype(int)
    return pd.DataFrame({"datetime": df["datetime"], "count": preds})


v2.masthead()
NAV_OPTIONS = ["Forecast", "Batch", "Insights", "About"]
requested = st.query_params.get("page", "Forecast")
nav_index = NAV_OPTIONS.index(requested) if requested in NAV_OPTIONS else 0
page = st.radio("Navigate", NAV_OPTIONS, horizontal=True, label_visibility="collapsed",
                index=nav_index, key="nav_page")

if page == "Forecast":
    s = st.session_state
    if isinstance(s["in_date"], str):
        s["in_date"] = pd.to_datetime(s["in_date"]).date()
    date0 = pd.to_datetime(s["in_date"]).strftime("%Y-%m-%d")
    t0, a0, h0, w0 = norm(float(s["in_t"]), float(s["in_t"]) + 2.0,
                          int(s["in_hum"]), int(s["in_wind"]))
    preview = forecast(date0, int(s["in_season"]), int(s["in_holiday"]),
                       int(s["in_workingday"]), int(s["in_weather"]), t0, a0, h0, w0)
    ph = int(np.argmax(preview))
    v2.hero("hourly ridership · capital bikeshare 2011–2012",
            "Read the city's rhythm.",
            "Twelve months of hourly rides, one fitted model. Set the conditions on the left "
            "and the whole day redraws itself on the right.",
            f"{preview[int(s['in_hour'])]:.0f}", f"{ph:02d}:00 · {preview[ph]:.0f} bikes", preview)

    v2.section("Shape the scenario", "controls scroll · results stay pinned")
    left, right = st.columns([0.9, 2.1], gap="large")
    with left:
        st.html('<div id="v2-controls" style="height:0"></div>')
        with st.container(border=True):
            v2.label("01 · WHEN")
            picked = st.date_input("Date", key="in_date")
            d_str = pd.to_datetime(picked).strftime("%Y-%m-%d")
            dow = pd.to_datetime(d_str).dayofweek
            hour = st.slider("Hour", 0, 23, key="in_hour")
            st.caption(f"{DOW[dow]} · " + ("weekend" if dow >= 5 else "weekday"))

            v2.label("02 · DAY TYPE")
            v2.label("Season")
            season = st.radio("Season", [1, 2, 3, 4], horizontal=True,
                              format_func=lambda x: SEASONS[x], label_visibility="collapsed",
                              key="in_season")
            v2.label("Weather")
            weather = st.radio("Weather", [1, 2, 3, 4], horizontal=True,
                               format_func=lambda x: WEATHER[x], label_visibility="collapsed",
                               key="in_weather")
            v2.label("Holiday")
            holiday = st.radio("Holiday", [0, 1], horizontal=True,
                               format_func=lambda x: "Yes" if x else "No", label_visibility="collapsed",
                               key="in_holiday")
            wd_auto = 0 if (holiday == 1 or dow >= 5) else 1
            v2.label("Working day")
            if "in_workingday" not in s:
                s["in_workingday"] = wd_auto
            workingday = st.radio("Working day", [0, 1], horizontal=True,
                                  format_func=lambda x: "Yes" if x else "No", label_visibility="collapsed",
                                  key="in_workingday")

            v2.label("03 · CONDITIONS")
            t_c = st.slider("Temperature °C", -8.0, 39.0, key="in_t")
            hum = st.slider("Humidity %", 0, 100, key="in_hum")
            wind = st.slider("Wind", 0, 67, key="in_wind")
            at_c = t_c + 2.0
            s["in_at"] = at_c

        with st.container(border=True):
            v2.label("QUICK SCENARIOS")
            for name, preset in PRESETS.items():
                st.button(name, use_container_width=True,
                          on_click=apply_preset, args=(preset,))

    temp, atemp, humidity, windspeed = norm(t_c, at_c, hum, wind)
    curve = forecast(d_str, season, holiday, workingday, weather, temp, atemp, humidity, windspeed)
    pred = max(0, int(round(curve[hour])))
    day_avg = float(np.mean(curve))
    peak_h, peak_v = int(np.argmax(curve)), float(max(curve))
    st.html(f'<div class="v2-hud"><span>{hour:02d}:00 forecast</span><b>{pred} bikes</b>'
            f'<span class="hud-peak">peak {peak_h:02d}:00 · {peak_v:.0f}</span></div>')
    if pred > 300:
        verdict, warm = "Extra bikes needed at this hour.", True
    elif pred > 100:
        verdict, warm = "Normal rebalancing covers this hour.", False
    else:
        verdict, warm = "Thin demand — hold stock for the next peak.", True

    with right:
        st.html('<div id="v2-results" style="height:0"></div>')
        with st.container(border=True):
            st.subheader("Demand through the day")
            v2.bars(curve)
            v2.note(f"<b>{DOW[dow]} {pd.to_datetime(d_str):%d %b}</b> · "
                    f"peak {peak_h:02d}:00 at {peak_v:.0f} bikes · daily average {day_avg:.0f} · "
                    f"selected hour {pred:.0f} ({pred-day_avg:+.0f} vs average)")

        with st.container(border=True):
            st.subheader("The week at a glance")
            st.caption("Seven days × 24 hours. The outlined tile is your selected hour.")
            base = pd.to_datetime(d_str)
            monday = base - pd.Timedelta(days=base.dayofweek)
            week = []
            for d in range(7):
                day = monday + pd.Timedelta(days=d)
                wd = 0 if day.dayofweek >= 5 else int(workingday)
                week.append(forecast(day.strftime("%Y-%m-%d"), season, 0, wd, weather,
                                     temp, atemp, humidity, windspeed))
            v2.heatmap(week, DOW, hour)

        c1, c2 = st.columns([1, 1], gap="large")
        with c1:
            with st.container(border=True):
                st.subheader("Weather sensitivity")
                st.caption("Same hour, four skies.")
                vals = [max(0.0, forecast(d_str, season, holiday, workingday, w,
                                          temp, atemp, humidity, windspeed)[hour])
                        for w in (1, 2, 3, 4)]
                v2.compare([WEATHER[w] for w in (1, 2, 3, 4)], vals, int(weather) - 1)
        with c2:
            with st.container(border=True):
                st.subheader("Fleet note")
                st.markdown(v2.tag(verdict, warm), unsafe_allow_html=True)
                v2.note(f"At <b>{hour:02d}:00</b> on a <b>{DOW[dow]}</b> with "
                        f"<b>{WEATHER[weather].lower()}</b>, the model expects <b>{pred} bikes</b>. "
                        f"Compare that with a daily average of {day_avg:.0f}.")


elif page == "Batch":
    v2.hero("bulk scoring", "A city in one file.",
            "Upload hourly records and score every row with the same model used above.",
            "—", "upload a CSV to begin", None,
            label="FILE READY", unit="awaiting upload", foot_label="Next step")
    v2.section("Score a file", "CSV columns: datetime, season, holiday, workingday, weather, temp, atemp, humidity, windspeed")
    left, right = st.columns([0.9, 2.1], gap="large")
    with left:
        with st.container(border=True):
            v2.label("SAMPLE")
            try:
                with open("data/test.csv", "rb") as fh:
                    st.download_button("Download test.csv", fh, "test.csv",
                                       use_container_width=True, type="primary")
            except FileNotFoundError:
                st.caption("Sample file unavailable.")
    with right:
        with st.container(border=True):
            f = st.file_uploader("Upload a CSV", type=["csv"])
            if f is not None:
                try:
                    out = score_upload(f)
                except ValueError as exc:
                    st.error(f"Could not score that file: {exc}")
                except Exception as exc:
                    st.error(f"Could not read that file: {exc}")
                else:
                    st.caption(f"{len(out):,} rows scored · average {out['count'].mean():.0f} · "
                               f"peak {out['count'].max():,}")
                    st.dataframe(out.head(15), use_container_width=True, hide_index=True)
                    st.download_button("Download predictions", out.to_csv(index=False),
                                       "submission.csv", use_container_width=True, type="primary")


elif page == "Insights":
    tr = load_train()
    tr["hour"] = tr["datetime"].dt.hour
    hourly = tr.groupby("hour")["count"].mean().tolist()
    v2.hero("from the training data", "What moves demand.",
            "Ten thousand eight hundred eighty-six hourly records. Hour of day dominates; "
            "weather and holidays write the footnotes.",
            f"{max(hourly):.0f}", "17:00 · 364 bikes", hourly,
            label="PEAK HOUR AVERAGE", unit="bikes / hour", foot_label="Busiest hour")
    v2.section("Signals", "the shape behind the predictions")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        with st.container(border=True):
            st.subheader("Hourly profile")
            v2.bars(hourly)
            v2.note("Commuter peaks at <b>08:00</b> and <b>17:00–18:00</b>.")
    with c2:
        with st.container(border=True):
            st.subheader("Weather penalty")
            vals = tr.groupby("weather")["count"].mean().tolist()
            v2.compare([WEATHER[w] for w in (1, 2, 3, 4)], vals, -1)
            v2.note("Clear skies rent most; storms empty the racks.")


else:
    v2.hero("under the hood", "A model, not a mystery.",
            "Gradient-boosted trees learned the hourly rhythm of Capital Bikeshare. "
            "Every number you see is a prediction from that fitted model.",
            "0.53", "RMSLE · lower is better", None,
            label="MODEL ERROR", unit="RMSLE", foot_label="Leaderboard top")
    v2.section("Leaderboard", "held-out hours")
    v2.leaderboard([("Ridge baseline", 1.18, False), ("Random Forest", 0.71, False),
                    ("XGBoost", 0.65, False), ("HistGradientBoosting", 0.53, True)])
    v2.section("Reproduce", "four commands")
    with st.container(border=True):
        st.code("pip install -r requirements-dev.txt\npython src/train.py\n"
                "python src/predict.py\nstreamlit run app_v2.py", language="bash")

st.html('<div class="v2-footer">BikeShare demand studio · Capital Bikeshare 2011–2012 · '
        'built with Streamlit</div>')
