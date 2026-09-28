"""Bike Sharing Demand — modern, tutorial-friendly Streamlit UI (theme-safe)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from src.features import add_features

st.set_page_config(page_title="Bike Sharing Demand", page_icon="🚲", layout="wide",
                   initial_sidebar_state="expanded")

SEASONS = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
SEASON_ICON = {1: "❄️", 2: "🌸", 3: "☀️", 4: "🍂"}
WEATHER = {1: "Clear / Few clouds", 2: "Mist + Cloudy", 3: "Light Snow / Rain", 4: "Heavy Rain / Snow"}
WEATHER_ICON = {1: "☀️", 2: "🌫️", 3: "🌧️", 4: "⛈️"}
WEATHER_TIP = {
    1: "Best biking weather — demand is highest.",
    2: "Slightly lower demand than clear days.",
    3: "Demand drops a lot — people avoid bikes.",
    4: "Very low demand — only a few riders.",
}
DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

PRESETS = {
    "🌅 Morning rush": dict(date="2012-06-15", hour=8, season=3, workingday=1, weather=1, t_c=20.0, hum=60, wind=10),
    "🌇 Evening rush": dict(date="2012-06-15", hour=18, season=3, workingday=1, weather=1, t_c=24.0, hum=55, wind=12),
    "🏖️ Weekend leisure": dict(date="2012-06-16", hour=14, season=3, workingday=0, weather=1, t_c=28.0, hum=50, wind=8),
    "🌧️ Rainy day": dict(date="2012-06-15", hour=9, season=2, workingday=1, weather=3, t_c=15.0, hum=85, wind=20),
}

@st.cache_resource
def load_model():
    b = joblib.load("src/model.pkl")
    return b["model"], b["features"]

@st.cache_data
def load_train():
    return pd.read_csv("data/train.csv", parse_dates=["datetime"])

model, FEATURES = load_model()

# ---------- sidebar ----------
with st.sidebar:
    st.title("🚲 BikeShare AI")
    st.caption("Demand prediction · internship project")
    page = st.radio("Navigate", ["🔮 Predict", "📤 Batch", "📊 Insights", "ℹ️ About"],
                    label_visibility="collapsed")
    st.divider()
    tut = st.toggle("📚 Tutorial guide", value=True,
                    help="ON adds step-by-step explanations. OFF gives a clean pro tool.")
    st.divider()
    st.subheader("⚡ Quick start")
    st.caption("Pick an example scenario:")
    cols = st.columns(2)
    for i, name in enumerate(PRESETS):
        with cols[i % 2]:
            if st.button(name, use_container_width=True):
                for k, v in PRESETS[name].items():
                    st.session_state[f"in_{k}"] = v
                st.session_state["nav_hint"] = name
    st.divider()
    st.caption("Model: HistGradientBoosting · RMSLE 0.53 · 10,886 hourly records (2011–2012)")

for k, v in {"in_date": "2012-06-15", "in_hour": 8, "in_season": 3, "in_workingday": 1,
             "in_weather": 1, "in_t": 22.0, "in_at": 24.0, "in_hum": 60, "in_wind": 12,
             "in_holiday": 0}.items():
    st.session_state.setdefault(k, v)

def norm_inputs(t_c, at_c, hum_pct, wind):
    return (t_c + 8) / 47.0, (at_c + 16) / 66.0, hum_pct / 100.0, wind / 67.0

def predict_row(dt, season, holiday, workingday, weather, temp, atemp, humidity, windspeed):
    row = add_features(pd.DataFrame([{
        "datetime": dt, "season": season, "holiday": holiday, "workingday": workingday,
        "weather": weather, "temp": temp, "atemp": atemp,
        "humidity": humidity, "windspeed": windspeed}]))
    return max(0, int(round(float(np.expm1(model.predict(row[FEATURES])[0])))))

def demand_verdict(pred):
    if pred > 300:
        return "HIGH demand — stage extra bikes.", "success"
    if pred > 100:
        return "MEDIUM demand — normal staffing.", "info"
    return "LOW demand — bad weather or off-hour.", "warning"

def show_verdict(pred):
    msg, kind = demand_verdict(pred)
    getattr(st, kind)(("✅ " if kind == "success" else "➖ " if kind == "info" else "🔻 ") + msg)

# ================= PREDICT =================
if page == "🔮 Predict":
    st.header("Predict Bike Demand")
    if tut:
        st.info("**3 steps:** ① WHEN → ② DAY TYPE → ③ WEATHER. Start from a sidebar preset, then tweak one thing and watch the result.")
    if st.session_state.get("nav_hint"):
        st.caption(f"Loaded preset: **{st.session_state.pop('nav_hint')}** — adjust below.")

    with st.container(border=True):
        st.subheader("Step 1 · When Will People Need Bikes?")
        c1, c2 = st.columns(2)
        with c1:
            d_str = st.date_input("Date", value=pd.to_datetime(st.session_state["in_date"]).date(),
                                  help="Weekday = commute peaks. Weekend = midday leisure peak.").strftime("%Y-%m-%d")
            st.session_state["in_date"] = d_str
            dow_auto = pd.to_datetime(d_str).dayofweek
            st.caption(f"That's a **{DOW[dow_auto]}** — {'weekend (leisure trips)' if dow_auto >= 5 else 'weekday (commute trips)'}.")
        with c2:
            h = st.slider("Hour of day", 0, 23, int(st.session_state["in_hour"]),
                          help="8am and 5–6pm are peaks (300+). 0–4am is near zero.")
            st.session_state["in_hour"] = h
            if h in (8, 17, 18):
                st.success("🔥 Rush hour — expect HIGH demand.")
            elif 0 <= h <= 4:
                st.warning("💤 Night — expect VERY LOW demand.")

    with st.container(border=True):
        st.subheader("Step 2 · What Kind of Day Is It?")
        c3, c4 = st.columns(2)
        with c3:
            season = st.selectbox("Season", [1, 2, 3, 4], index=[1, 2, 3, 4].index(int(st.session_state["in_season"])),
                                  format_func=lambda x: f"{SEASON_ICON[x]} {SEASONS[x]}",
                                  help="Summer rents most, winter least.")
            st.session_state["in_season"] = season
            weather = st.selectbox("Weather", [1, 2, 3, 4], index=[1, 2, 3, 4].index(int(st.session_state["in_weather"])),
                                   format_func=lambda x: f"{WEATHER_ICON[x]} {WEATHER[x]}",
                                   help="Weather is the biggest demand lever after hour.")
            st.session_state["in_weather"] = weather
            if tut:
                st.info(f"💡 {WEATHER_TIP[weather]}")
        with c4:
            holiday = st.segmented_control("Holiday?", [0, 1], default=int(st.session_state["in_holiday"]),
                                           format_func=lambda x: "Yes 🎉" if x else "No",
                                           help="Holidays behave like weekends.")
            st.session_state["in_holiday"] = holiday
            wd_auto = 0 if (holiday == 1 or dow_auto >= 5) else 1
            workingday = st.segmented_control("Working day?", [0, 1], default=wd_auto,
                                              format_func=lambda x: "Yes 💼" if x else "No 🏖️",
                                              help="Working day = weekday AND not a holiday.")
            st.session_state["in_workingday"] = workingday

    with st.container(border=True):
        st.subheader("Step 3 · Weather Details (Real Units)")
        if tut:
            st.caption("Experiment: set 22°C + 60% humidity, note the result, then raise humidity to 90% and watch it fall.")
        w1, w2, w3, w4 = st.columns(4)
        with w1:
            t_c = st.slider("🌡️ Temp (°C)", -8.0, 39.0, float(st.session_state["in_t"]), help="20–28°C is the sweet spot.")
        with w2:
            at_c = st.slider("🥵 Feels-like (°C)", -16.0, 50.0, float(st.session_state["in_at"]))
        with w3:
            hum_pct = st.slider("💧 Humidity (%)", 0, 100, int(st.session_state["in_hum"]), help="Above 80% demand drops.")
        with w4:
            wind = st.slider("💨 Wind (0–67)", 0, 67, int(st.session_state["in_wind"]), help="Above 30 discourages cycling.")
        st.session_state.update({"in_t": t_c, "in_at": at_c, "in_hum": hum_pct, "in_wind": wind})

    temp, atemp, humidity, windspeed = norm_inputs(t_c, at_c, hum_pct, wind)
    dt = pd.to_datetime(f"{d_str} {h:02d}:00")
    pred = predict_row(dt, season, holiday, workingday, weather, temp, atemp, humidity, windspeed)

    st.divider()
    hrs = add_features(pd.DataFrame([{
        "datetime": pd.to_datetime(f"{d_str} {hh:02d}:00"), "season": season, "holiday": holiday,
        "workingday": workingday, "weather": weather, "temp": temp, "atemp": atemp,
        "humidity": humidity, "windspeed": windspeed} for hh in range(24)]))
    hrs["predicted"] = np.expm1(model.predict(hrs[FEATURES])).clip(min=0)
    day_avg = float(hrs["predicted"].mean())
    peak_h = int(hrs["predicted"].idxmax())
    peak_v = float(hrs["predicted"].max())

    r1, r2 = st.columns([1, 2])
    with r1:
        with st.container(border=True):
            st.metric(f"{DOW[dow_auto]} {dt:%b %d, %H:00} · {SEASONS[season]}", f"{pred} bikes",
                      delta=f"{pred - day_avg:+.0f} vs day avg")
            show_verdict(pred)
        if tut:
            with st.expander("🧒 Explain like I'm 5"):
                st.write(f"At **{h}:00 on a {DOW[dow_auto]}** with **{WEATHER[weather]}**, "
                         f"{'commuters' if workingday else 'leisure riders'} need about **{pred} bikes**.")
    with r2:
        with st.container(border=True):
            st.subheader("24-Hour Curve — Same Conditions")
            st.caption("Move the Hour slider and watch this shift. Workdays show twin commute bumps.")
            st.line_chart(hrs.set_index(hrs["datetime"].dt.hour)["predicted"], height=240)
            st.caption(f"Day peak: {peak_h}:00 — {peak_v:.0f} bikes · daily avg {day_avg:.0f}.")

# ================= BATCH =================
elif page == "📤 Batch":
    st.header("Batch Predictions")
    if tut:
        st.info("**Steps:** ① download the sample → ② upload it → ③ download predictions. No code needed.")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("① Sample file")
            try:
                with open("data/test.csv", "rb") as fh:
                    st.download_button("⬇ Download test.csv", fh, "test.csv", use_container_width=True)
            except FileNotFoundError:
                st.warning("data/test.csv not found.")
        with c2:
            st.subheader("② Upload & predict")
            f = st.file_uploader("CSV with datetime,season,holiday,workingday,weather,temp,atemp,humidity,windspeed",
                                 type=["csv"], label_visibility="collapsed")
    if f is not None:
        bdf = add_features(pd.read_csv(f, parse_dates=["datetime"]))
        preds = np.expm1(model.predict(bdf[FEATURES])).clip(min=0).round().astype(int)
        out = pd.DataFrame({"datetime": bdf["datetime"], "count": preds})
        m1, m2, m3 = st.columns(3)
        m1.metric("Rows predicted", f"{len(out):,}")
        m2.metric("Avg bikes/hour", f"{preds.mean():.0f}")
        m3.metric("Peak prediction", f"{preds.max():,}")
        with st.container(border=True):
            st.dataframe(out.head(20), use_container_width=True)
            st.line_chart(out.set_index("datetime")["count"])
            st.download_button("③ ⬇ Download submission.csv", out.to_csv(index=False),
                               "submission.csv", use_container_width=True)

# ================= INSIGHTS =================
elif page == "📊 Insights":
    st.header("What Drives Demand?")
    if tut:
        st.info("Read each card, guess the pattern, then verify it on the Predict page.")
    tr = load_train()
    tr["hour"] = tr["datetime"].dt.hour
    tr["dow"] = tr["datetime"].dt.dayofweek
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader("Rush Hours Rule")
            st.bar_chart(tr.groupby("hour")["count"].mean())
            st.caption("Peaks at 8am + 5–6pm. Try 4am vs 6pm in Predict.")
    with c2:
        with st.container(border=True):
            st.subheader("Weekday vs Weekend")
            by_dow = tr.groupby("dow")["count"].mean()
            by_dow.index = [DOW[i] for i in by_dow.index]
            st.bar_chart(by_dow)
            st.caption("Weekends peak midday, not at 8am.")
    c3, c4 = st.columns(2)
    with c3:
        with st.container(border=True):
            st.subheader("Weather Penalty")
            st.bar_chart(tr.groupby("weather")["count"].mean())
            st.caption("1 = clear (best) → 4 = storm (worst).")
    with c4:
        with st.container(border=True):
            st.subheader("Temperature Sweet Spot")
            st.scatter_chart(tr.sample(min(2000, len(tr)))[["temp", "count"]].set_index("temp"))
            st.caption("Demand climbs to ~20°C then flattens.")

# ================= ABOUT =================
else:
    st.header("How It Works")
    if tut:
        st.info("The model studied **10,886 past hours** and learned rules like '5pm + sunny + workday = busy'.")
    with st.container(border=True):
        st.subheader("Model Leaderboard")
        st.dataframe(pd.DataFrame([
            {"Model": "Ridge (baseline)", "RMSLE ↓": 1.18},
            {"Model": "RandomForest-100", "RMSLE ↓": 0.71},
            {"Model": "XGBoost (500 trees)", "RMSLE ↓": 0.65},
            {"Model": "HistGradientBoosting ✅ deployed", "RMSLE ↓": 0.53},
        ]), use_container_width=True, hide_index=True)
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader("📖 Glossary")
            st.markdown("- **RMSLE** — error metric, lower is better.\n"
                        "- **workingday** — 1 = office day, 0 = weekend/holiday.\n"
                        "- **temp scale** — UI takes °C, converts to 0–1 for the model.")
    with c2:
        with st.container(border=True):
            st.subheader("💻 Reproduce")
            st.code("pip install -r requirements.txt\npython src/train.py\npython src/predict.py\nstreamlit run app.py", language="bash")

st.divider()
st.caption("Bike Sharing Demand · Capital Bikeshare 2011–2012 · UCI / Kaggle · Built with Streamlit")
