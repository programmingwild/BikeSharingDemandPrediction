"""Bike Sharing Demand — cycle demand intelligence console."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from src.features import add_features
import ui

st.set_page_config(page_title="Cadence · BikeShare Intelligence", page_icon="🚲",
                   layout="wide", initial_sidebar_state="expanded")
ui.inject()

SEASONS = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
SEASON_ICON = {1: "❄️", 2: "🌸", 3: "☀️", 4: "🍂"}
WEATHER = {1: "Clear / Few clouds", 2: "Mist + Cloudy", 3: "Light Snow / Rain", 4: "Heavy Rain / Snow"}
WEATHER_ICON = {1: "☀️", 2: "🌫️", 3: "🌧️", 4: "⛈️"}
WEATHER_TIP = {
    1: "Clear skies — demand is at its strongest.",
    2: "A little haze takes a small bite out of ridership.",
    3: "Rain or snow keeps many people indoors.",
    4: "Severe weather all but empties the racks.",
}
DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

PRESETS = {
    "🌅 Morning rush": dict(date="2012-06-15", hour=8, season=3, workingday=1, weather=1, t_c=20.0, hum=60, wind=10),
    "🌇 Evening rush": dict(date="2012-06-15", hour=18, season=3, workingday=1, weather=1, t_c=24.0, hum=55, wind=12),
    "🏖️ Weekend leisure": dict(date="2012-06-16", hour=14, season=3, workingday=0, weather=1, t_c=28.0, hum=50, wind=8),
    "🌧️ Rainy day": dict(date="2012-06-15", hour=9, season=2, workingday=1, weather=3, t_c=15.0, hum=85, wind=20),
}

DEFAULTS = {"in_date": "2012-06-15", "in_hour": 8, "in_season": 3, "in_workingday": 1,
            "in_weather": 1, "in_t": 22.0, "in_at": 24.0, "in_hum": 60, "in_wind": 12,
            "in_holiday": 0}
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)


@st.cache_resource
def load_model():
    b = joblib.load("src/model.pkl")
    return b["model"], b["features"]


@st.cache_data
def load_train():
    return pd.read_csv("data/train.csv", parse_dates=["datetime"])


model, FEATURES = load_model()


def norm_inputs(t_c, at_c, hum_pct, wind):
    return (t_c + 8) / 47.0, (at_c + 16) / 66.0, hum_pct / 100.0, wind / 67.0


def build_row(d_str, hh, season, holiday, workingday, weather, temp, atemp, humidity, windspeed):
    return add_features(pd.DataFrame([{
        "datetime": pd.to_datetime(f"{d_str} {hh:02d}:00"), "season": season,
        "holiday": holiday, "workingday": workingday, "weather": weather,
        "temp": temp, "atemp": atemp, "humidity": humidity, "windspeed": windspeed}]))


def day_curve(d_str, season, holiday, workingday, weather, temp, atemp, humidity, windspeed):
    hours = add_features(pd.DataFrame([{
        "datetime": pd.to_datetime(f"{d_str} {hh:02d}:00"), "season": season,
        "holiday": holiday, "workingday": workingday, "weather": weather,
        "temp": temp, "atemp": atemp, "humidity": humidity, "windspeed": windspeed}
        for hh in range(24)]))
    hours["predicted"] = np.expm1(model.predict(hours[FEATURES])).clip(min=0)
    return hours


def predict_row(row):
    return max(0, int(round(float(np.expm1(model.predict(row[FEATURES])[0])))))


def demand_verdict(pred):
    if pred > 300:
        return "High demand — stage extra bikes.", "ok"
    if pred > 100:
        return "Steady demand — normal staffing.", "warn"
    return "Low demand — off-hour or rough weather.", "low"


# --------------------------------------------------------------------------- sidebar
with st.sidebar:
    st.html(f"""
<div style="display:flex;align-items:center;gap:12px;margin:2px 0 6px">
  {ui.brand_mark()}
  <div>
    <div style="font-family:'Space Grotesk',sans-serif;font-size:1.3rem;font-weight:600;letter-spacing:-.05em;line-height:1">cadence</div>
    <div style="font-size:.68rem;color:var(--muted);letter-spacing:.03em;margin-top:5px">cycle demand intelligence</div>
  </div>
</div>""")
    st.divider()
    page = st.radio("Navigate", ["🔮 Predict", "📤 Batch", "📊 Insights", "ℹ️ About"],
                    label_visibility="collapsed")
    st.divider()
    tut = st.toggle("Tutorial guide", value=True,
                    help="On adds step-by-step explanations. Off gives a clean pro tool.")
    st.divider()
    st.caption("QUICK SCENARIOS")
    cols = st.columns(2)
    for i, name in enumerate(PRESETS):
        with cols[i % 2]:
            if st.button(name, use_container_width=True):
                for k, v in PRESETS[name].items():
                    st.session_state[f"in_{k}"] = v
                st.session_state["nav_hint"] = name
    st.divider()
    st.caption("HistGradientBoosting · RMSLE 0.53\n10,886 hourly rides · 2011–2012")


# =============================================================== PREDICT
if page == "🔮 Predict":
    # Render the hero from current widget state so it reacts on every rerun.
    s = st.session_state
    temp0, atemp0, hum0, wind0 = norm_inputs(s["in_t"], s["in_at"], s["in_hum"], s["in_wind"])
    hours0 = day_curve(s["in_date"], int(s["in_season"]), int(s["in_holiday"]),
                       int(s["in_workingday"]), int(s["in_weather"]),
                       temp0, atemp0, hum0, wind0)
    peak_h0 = int(hours0["predicted"].idxmax())
    peak_v0 = float(hours0["predicted"].max())

    ui.hero(
        "live hourly forecast",
        "Where the city needs bikes next.",
        "An hourly demand model trained on two years of Capital Bikeshare rides. "
        "Change a single condition and watch the whole day respond.",
        curve=hours0["predicted"].tolist(),
        peak_label=f"peak {peak_h0:02d}:00 · {peak_v0:.0f} bikes",
    )
    if s.get("nav_hint"):
        st.caption(f"Loaded scenario: **{s.pop('nav_hint')}** — adjust anything below.")

    ui.section("Scenario builder", "three inputs · one live forecast")
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            ui.step("01", "When", "date & hour")
            d_str = st.date_input("Date", value=pd.to_datetime(s["in_date"]).date(),
                                  help="Weekdays bring commute peaks; weekends peak at midday.").strftime("%Y-%m-%d")
            s["in_date"] = d_str
            dow_auto = pd.to_datetime(d_str).dayofweek
            st.caption(f"{DOW[dow_auto]} — " +
                       ("weekend, leisure trips" if dow_auto >= 5 else "weekday, commute trips"))
            h = st.slider("Hour of day", 0, 23, int(s["in_hour"]),
                          help="8am and 5–6pm are the commuter peaks.")
            s["in_hour"] = h
            if h in (8, 17, 18):
                st.caption("🔥 Rush hour — expect high demand.")
            elif 0 <= h <= 4:
                st.caption("💤 Overnight — demand is near zero.")
    with c2:
        with st.container(border=True):
            ui.step("02", "Day type", "season & weather")
            season = st.selectbox("Season", [1, 2, 3, 4],
                                  index=[1, 2, 3, 4].index(int(s["in_season"])),
                                  format_func=lambda x: f"{SEASON_ICON[x]} {SEASONS[x]}")
            s["in_season"] = season
            weather = st.selectbox("Weather", [1, 2, 3, 4],
                                   index=[1, 2, 3, 4].index(int(s["in_weather"])),
                                   format_func=lambda x: f"{WEATHER_ICON[x]} {WEATHER[x]}")
            s["in_weather"] = weather
            if tut:
                st.caption(f"💡 {WEATHER_TIP[weather]}")
            holiday = st.segmented_control("Holiday?", [0, 1], default=int(s["in_holiday"]),
                                           format_func=lambda x: "Yes 🎉" if x else "No")
            s["in_holiday"] = holiday
            wd_auto = 0 if (holiday == 1 or dow_auto >= 5) else 1
            workingday = st.segmented_control("Working day?", [0, 1], default=wd_auto,
                                              format_func=lambda x: "Yes 💼" if x else "No 🏖️")
            s["in_workingday"] = workingday

    with st.container(border=True):
        ui.step("03", "Conditions", "degrees, humidity, wind")
        w1, w2, w3, w4 = st.columns(4)
        with w1:
            t_c = st.slider("🌡️ Temp (°C)", -8.0, 39.0, float(s["in_t"]))
        with w2:
            at_c = st.slider("🥵 Feels like (°C)", -16.0, 50.0, float(s["in_at"]))
        with w3:
            hum_pct = st.slider("💧 Humidity (%)", 0, 100, int(s["in_hum"]))
        with w4:
            wind = st.slider("💨 Wind (0–67)", 0, 67, int(s["in_wind"]))
        s.update({"in_t": t_c, "in_at": at_c, "in_hum": hum_pct, "in_wind": wind})

    temp, atemp, humidity, windspeed = norm_inputs(t_c, at_c, hum_pct, wind)
    row = build_row(d_str, h, season, holiday, workingday, weather, temp, atemp, humidity, windspeed)
    pred = predict_row(row)
    hours = day_curve(d_str, season, holiday, workingday, weather, temp, atemp, humidity, windspeed)
    day_avg = float(hours["predicted"].mean())
    peak_h = int(hours["predicted"].idxmax())
    peak_v = float(hours["predicted"].max())
    verdict, tone = demand_verdict(pred)

    ui.section("Forecast", f"{DOW[dow_auto]} {pd.to_datetime(d_str):%b %d} · {SEASONS[season]}")
    r1, r2 = st.columns([1, 1.35])
    with r1:
        ui.readout(
            pred, "bikes expected", ui.chip(verdict, tone),
            [("Day average", f"{day_avg:.0f}", ""),
             ("Peak hour", f"{peak_h:02d}:00 · {peak_v:.0f}", "amber"),
             ("vs. day avg", f"{pred - day_avg:+.0f}", "mint" if pred >= day_avg else ""),
             ],
            "Model confidence: RMSLE 0.53 on held-out hours.",
        )
        if tut:
            with st.expander("Explain like I'm five"):
                st.write(f"At **{h}:00 on a {DOW[dow_auto]}** with **{WEATHER[weather]}**, "
                         f"{'commuters' if workingday else 'leisure riders'} need about **{pred} bikes**.")
    with r2:
        with st.container(border=True):
            st.subheader("Same conditions, all 24 hours")
            st.caption("The twin commute bumps are the model's strongest signature.")
            st.line_chart(hours.set_index(hours["datetime"].dt.hour)["predicted"], height=250)
            st.caption(f"Daily peak {peak_h:02d}:00 · {peak_v:.0f} bikes · average {day_avg:.0f}.")


# =============================================================== BATCH
elif page == "📤 Batch":
    ui.hero("bulk scoring", "A whole city, one file.",
            "Upload hourly records and get a prediction for every row. "
            "The same model powers the live forecast — no setup, no code.")
    ui.section("Score your file", "download → upload → download")
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            ui.step("01", "Sample file", "start here")
            st.caption("Grab the sample to see the exact columns the model expects.")
            try:
                with open("data/test.csv", "rb") as fh:
                    st.download_button("⬇ Download test.csv", fh, "test.csv",
                                       use_container_width=True, type="primary")
            except FileNotFoundError:
                st.caption("Sample file not available.")
    with c2:
        with st.container(border=True):
            ui.step("02", "Upload & predict", "your data")
            st.caption("CSV with datetime, season, holiday, workingday, weather, temp, atemp, humidity, windspeed.")
            f = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")

    if f is not None:
        bdf = add_features(pd.read_csv(f, parse_dates=["datetime"]))
        preds = np.expm1(model.predict(bdf[FEATURES])).clip(min=0).round().astype(int)
        out = pd.DataFrame({"datetime": bdf["datetime"], "count": preds})
        ui.section("Results", f"{len(out):,} rows scored")
        ui.readout(
            f"{preds.mean():.0f}", "bikes / hour on average",
            ui.chip(f"peak {preds.max():,}", "amber"),
            [("Rows scored", f"{len(out):,}", ""),
             ("Peak hour", f"{preds.max():,}", "mint"),
             ("Quiet hour", f"{preds.min():,}", ""),
             ],
        )
        with st.container(border=True):
            st.caption("First 20 predictions")
            st.dataframe(out.head(20), use_container_width=True, hide_index=True)
            st.line_chart(out.set_index("datetime")["count"], height=260)
            st.download_button("⬇ Download submission.csv", out.to_csv(index=False),
                               "submission.csv", use_container_width=True, type="primary")


# =============================================================== INSIGHTS
elif page == "📊 Insights":
    tr = load_train()
    tr["hour"] = tr["datetime"].dt.hour
    tr["dow"] = tr["datetime"].dt.dayofweek
    hourly = tr.groupby("hour")["count"].mean()
    ui.hero("from the data", "What moves demand.",
            "Ten thousand eight hundred eighty-six hourly records, stripped of guesswork. "
            "Hour of day dominates; weather writes the footnotes.",
            curve=hourly.tolist(), peak_label=f"busiest hour · {int(hourly.idxmax()):02d}:00")
    ui.section("Signals", "read a card, then test it on Predict")
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            ui.step("01", "Rush hours rule", "commute peaks")
            st.bar_chart(tr.groupby("hour")["count"].mean())
            st.caption("Peaks at 8am and 5–6pm. Compare 4am with 6pm on Predict.")
    with c2:
        with st.container(border=True):
            ui.step("02", "Weekday ≠ weekend", "different shapes")
            by_dow = tr.groupby("dow")["count"].mean()
            by_dow.index = [DOW[i] for i in by_dow.index]
            st.bar_chart(by_dow)
            st.caption("Weekends peak at midday instead of at 8am.")
    c3, c4 = st.columns(2)
    with c3:
        with st.container(border=True):
            ui.step("03", "Weather penalty", "rain empties racks")
            st.bar_chart(tr.groupby("weather")["count"].mean())
            st.caption("1 = clear, 4 = storm. The drop is steep and immediate.")
    with c4:
        with st.container(border=True):
            ui.step("04", "Temperature sweet spot", "comfort wins")
            st.scatter_chart(tr.sample(min(2000, len(tr)))[["temp", "count"]].set_index("temp"))
            st.caption("Ridership climbs toward 20°C, then flattens.")


# =============================================================== ABOUT
else:
    ui.hero("under the hood", "How the model thinks.",
            "A gradient-boosted tree model learned the rhythm of hourly ridership. "
            "It beats the alternatives by a wide margin, and every input you change "
            "flows through the same fitted trees.")
    ui.section("Leaderboard", "RMSLE · lower is better")
    ui.leaderboard([
        ("Ridge · baseline", 1.18, False),
        ("Random Forest · 100 trees", 0.71, False),
        ("XGBoost · 500 trees", 0.65, False),
        ("HistGradientBoosting", 0.53, True),
    ])
    ui.section("The essentials", "short version")
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            ui.step("A", "Glossary", "plain language")
            st.caption("**RMSLE** — prediction error on a log scale; lower is better.")
            st.caption("**Working day** — weekday and not a holiday.")
            st.caption("**Temp scale** — the UI takes °C and converts to 0–1 for the model.")
    with c2:
        with st.container(border=True):
            ui.step("B", "Reproduce", "four commands")
            st.code("pip install -r requirements-dev.txt\npython src/train.py\n"
                    "python src/predict.py\nstreamlit run streamlit_app.py", language="bash")

st.caption("cadence · Capital Bikeshare 2011–2012 · built with Streamlit")
