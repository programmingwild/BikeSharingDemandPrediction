"""Metro Demand Studio — a separate premium UI. Streamlit is the backend.

This file does not touch streamlit_app.py. Deploy by setting Streamlit Cloud's
"Main file path" to app_v2.py, or run locally with: streamlit run app_v2.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from src.features import add_features
import ui_v2 as v2

st.set_page_config(page_title="Metro · Demand Studio", page_icon="🚇",
                   layout="wide", initial_sidebar_state="collapsed")
v2.inject()

SEASONS = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
WEATHER = {1: "Clear", 2: "Mist", 3: "Light rain / snow", 4: "Heavy rain / snow"}
DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
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


v2.masthead()
page = st.radio("Navigate", ["Forecast", "Batch", "Insights", "About"],
                horizontal=True, label_visibility="collapsed")

if page == "Forecast":
    s = st.session_state
    t0, a0, h0, w0 = norm(s["in_t"], s["in_at"], s["in_hum"], s["in_wind"])
    preview = forecast(s["in_date"], int(s["in_season"]), int(s["in_holiday"]),
                       int(s["in_workingday"]), int(s["in_weather"]), t0, a0, h0, w0)
    ph = int(np.argmax(preview))
    v2.hero("hourly ridership · capital bikeshare 2011–2012",
            "Read the city's rhythm.",
            "Twelve months of hourly rides, one fitted model. Set the conditions on the left "
            "and the whole day redraws itself on the right.",
            f"{preview[int(s['in_hour'])]:.0f}", f"{ph:02d}:00 · {preview[ph]:.0f} bikes", preview)

    v2.section("Shape the scenario", "change one thing and watch the response")
    left, right = st.columns([0.9, 2.1], gap="large")
    with left:
        with st.container(border=True):
            v2.label("01 · WHEN")
            d_str = st.date_input("Date", value=pd.to_datetime(s["in_date"]).date()).strftime("%Y-%m-%d")
            s["in_date"] = d_str
            dow = pd.to_datetime(d_str).dayofweek
            hour = st.slider("Hour", 0, 23, int(s["in_hour"]))
            s["in_hour"] = hour
            st.caption(f"{DOW[dow]} · " + ("weekend" if dow >= 5 else "weekday"))

            v2.label("02 · DAY TYPE")
            season = st.selectbox("Season", [1, 2, 3, 4],
                                  index=[1, 2, 3, 4].index(int(s["in_season"])),
                                  format_func=lambda x: SEASONS[x])
            s["in_season"] = season
            weather = st.selectbox("Weather", [1, 2, 3, 4],
                                   index=[1, 2, 3, 4].index(int(s["in_weather"])),
                                   format_func=lambda x: WEATHER[x])
            s["in_weather"] = weather
            holiday = st.segmented_control("Holiday", [0, 1], default=int(s["in_holiday"]),
                                           format_func=lambda x: "Yes" if x else "No")
            s["in_holiday"] = holiday
            wd_auto = 0 if (holiday == 1 or dow >= 5) else 1
            workingday = st.segmented_control("Working day", [0, 1], default=wd_auto,
                                              format_func=lambda x: "Yes" if x else "No")
            s["in_workingday"] = workingday

            v2.label("03 · CONDITIONS")
            t_c = st.slider("Temperature °C", -8.0, 39.0, float(s["in_t"]))
            hum = st.slider("Humidity %", 0, 100, int(s["in_hum"]))
            wind = st.slider("Wind", 0, 67, int(s["in_wind"]))
            at_c = t_c + 2.0
            s.update(in_t=t_c, in_at=at_c, in_hum=hum, in_wind=wind)

        with st.container(border=True):
            v2.label("QUICK SCENARIOS")
            for name, preset in PRESETS.items():
                if st.button(name, use_container_width=True):
                    for k, val in preset.items():
                        s[f"in_{k}"] = val
                    s["in_at"] = preset["t_c"] + 2.0
                    st.rerun()

    temp, atemp, humidity, windspeed = norm(t_c, at_c, hum, wind)
    curve = forecast(d_str, season, holiday, workingday, weather, temp, atemp, humidity, windspeed)
    pred = max(0, int(round(curve[hour])))
    day_avg = float(np.mean(curve))
    peak_h, peak_v = int(np.argmax(curve)), float(max(curve))
    if pred > 300:
        verdict, warm = "Extra bikes needed at this hour.", True
    elif pred > 100:
        verdict, warm = "Normal rebalancing covers this hour.", False
    else:
        verdict, warm = "Thin demand — hold stock for the next peak.", True

    with right:
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
            "—", "upload a CSV to begin", [1] * 24,
            label="FILE READY", unit="awaiting upload")
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
                df = add_features(pd.read_csv(f, parse_dates=["datetime"]))
                preds = np.expm1(model.predict(df[FEATURES])).clip(min=0).round().astype(int)
                out = pd.DataFrame({"datetime": df["datetime"], "count": preds})
                st.caption(f"{len(out):,} rows scored · average {preds.mean():.0f} · peak {preds.max():,}")
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
            f"{max(hourly):.0f}", "busiest hour · 17:00", hourly,
            label="PEAK HOUR AVERAGE", unit="bikes / hour")
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
            "0.53", "RMSLE · lower is better",
            [1, 2, 3, 4, 5, 6, 5, 4, 6, 8, 9, 7, 6, 7, 9, 10, 8, 6, 4, 3, 2, 2, 1, 1],
            label="MODEL ERROR", unit="RMSLE")
    v2.section("Leaderboard", "held-out hours")
    v2.leaderboard([("Ridge baseline", 1.18, False), ("Random Forest", 0.71, False),
                    ("XGBoost", 0.65, False), ("HistGradientBoosting", 0.53, True)])
    v2.section("Reproduce", "four commands")
    with st.container(border=True):
        st.code("pip install -r requirements-dev.txt\npython src/train.py\n"
                "python src/predict.py\nstreamlit run app_v2.py", language="bash")

st.html('<div class="v2-footer">metro demand studio · Capital Bikeshare 2011–2012 · '
        'a separate UI backed by the same Streamlit model</div>')
