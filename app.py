"""Bike Sharing Demand — premium tutorial UI (theme-safe, skill-directed).

Art direction: "transit instrument, not dashboard" (Soft Structuralism).
Hero = the live prediction numeral. Quiet chrome everywhere else.
No hard-coded colors anywhere: every surface inherits the Streamlit theme,
so light and dark mode both render correctly.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from src.features import add_features

st.set_page_config(page_title="BikeShare AI — Demand Prediction", page_icon="🚲",
                   layout="wide", initial_sidebar_state="expanded")

# ---------- theme-safe premium CSS (typography + spacing only, zero colors) ----------
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
html, body, [class*="st-"], [class*="css-"] {
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
h1, h2, h3 { text-wrap: balance; letter-spacing: -0.02em; }
.eyebrow {
  text-transform: uppercase; letter-spacing: 0.22em;
  font-size: 11px; font-weight: 600; opacity: 0.6; margin-bottom: 0.15rem;
}
.hero-num { font-size: clamp(3rem, 7vw, 5rem); font-weight: 800;
  letter-spacing: -0.04em; line-height: 1; font-variant-numeric: tabular-nums; }
[data-testid="stMetricValue"] { font-variant-numeric: tabular-nums; }
.block-container { padding-top: 2rem; }
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
</style>
""", unsafe_allow_html=True)

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

for k, v in {"in_date": "2012-06-15", "in_hour": 8, "in_season": 3, "in_workingday": 1,
             "in_weather": 1, "in_t": 22.0, "in_at": 24.0, "in_hum": 60, "in_wind": 12,
             "in_holiday": 0}.items():
    st.session_state.setdefault(k, v)

def eyebrow(text: str):
    st.markdown(f'<p class="eyebrow">{text}</p>', unsafe_allow_html=True)

def norm_inputs(t_c, at_c, hum_pct, wind):
    return (t_c + 8) / 47.0, (at_c + 16) / 66.0, hum_pct / 100.0, wind / 67.0

def predict_row(dt, season, holiday, workingday, weather, temp, atemp, humidity, windspeed):
    row = add_features(pd.DataFrame([{
        "datetime": dt, "season": season, "holiday": holiday, "workingday": workingday,
        "weather": weather, "temp": temp, "atemp": atemp,
        "humidity": humidity, "windspeed": windspeed}]))
    return max(0, int(round(float(np.expm1(model.predict(row[FEATURES])[0])))))

def show_verdict(pred: int):
    if pred > 300:
        st.success("High demand — stage extra bikes at stations.")
    elif pred > 100:
        st.info("Medium demand — normal staffing.")
    else:
        st.warning("Low demand — bad weather or off-hour.")

# ---------- sidebar ----------
with st.sidebar:
    eyebrow("BikeShare AI · Transit Instrument")
    st.title("Demand Prediction")
    st.caption("Capital Bikeshare · 2011–2012 · Internship build")
    page = st.radio("Section", ["Predict", "Batch", "Insights", "About"],
                    label_visibility="collapsed")
    st.divider()
    tut = st.toggle("Tutorial guide", value=True,
                    help="On adds step-by-step coaching. Off gives a clean pro tool.")
    st.divider()
    eyebrow("Quick start")
    st.caption("Load a scenario, then tweak one variable:")
    cols = st.columns(2)
    for i, name in enumerate(PRESETS):
        with cols[i % 2]:
            if st.button(name, use_container_width=True):
                for k, v in PRESETS[name].items():
                    st.session_state[f"in_{k}"] = v
                st.session_state["nav_hint"] = name
    st.divider()
    st.caption("HistGradientBoosting · RMSLE 0.53 · 10,886 hourly records")

# ================= PREDICT =================
if page == "Predict":
    eyebrow("Live forecast · Washington D.C.")
    st.title("How many bikes will the city need?")
    st.write("Set the conditions. The forecast updates instantly — start from a preset, "
             "then move one slider and watch demand respond.")
    if st.session_state.get("nav_hint"):
        st.caption(f"Loaded scenario: **{st.session_state.pop('nav_hint')}**.")
    if tut:
        st.info("Three steps: **When** → **Day type** → **Weather**. Each card ends in the forecast below.")

    k1, k2, k3 = st.columns(3)
    k1.metric("Model error (RMSLE)", "0.53", "best of 4 tried")
    k2.metric("Training history", "10,886 hrs", "2 years")
    k3.metric("System peak", "5 PM", "≈ 870 bikes")

    with st.container(border=True):
        with st.container(border=True):
            eyebrow("Step 1 · When")
            c1, c2 = st.columns(2)
            with c1:
                d_str = st.date_input("Date", value=pd.to_datetime(st.session_state["in_date"]).date(),
                                      help="Weekday brings commute peaks. Weekend brings a midday leisure peak.").strftime("%Y-%m-%d")
                st.session_state["in_date"] = d_str
                dow_auto = pd.to_datetime(d_str).dayofweek
                st.caption(f"That's a **{DOW[dow_auto]}** — {'leisure trips' if dow_auto >= 5 else 'commute trips'}.")
            with c2:
                h = st.slider("Hour of day", 0, 23, int(st.session_state["in_hour"]),
                              help="8 AM and 5–6 PM peak above 300 bikes. 0–4 AM is near zero.")
                st.session_state["in_hour"] = h
                if h in (8, 17, 18):
                    st.success("Rush hour — expect high demand.")
                elif 0 <= h <= 4:
                    st.warning("Night — expect very low demand.")

    with st.container(border=True):
        with st.container(border=True):
            eyebrow("Step 2 · Day type")
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
                    st.info(f"{WEATHER_TIP[weather]}")
            with c4:
                holiday = st.segmented_control("Holiday?", [0, 1], default=int(st.session_state["in_holiday"]),
                                               format_func=lambda x: "Yes" if x else "No",
                                               help="Holidays behave like weekends.")
                st.session_state["in_holiday"] = holiday
                wd_auto = 0 if (holiday == 1 or dow_auto >= 5) else 1
                workingday = st.segmented_control("Working day?", [0, 1], default=wd_auto,
                                                  format_func=lambda x: "Yes" if x else "No",
                                                  help="A working day is a weekday that is not a holiday.")
                st.session_state["in_workingday"] = workingday

    with st.container(border=True):
        with st.container(border=True):
            eyebrow("Step 3 · Weather detail")
            if tut:
                st.caption("Experiment: note the forecast at 22°C / 60% humidity, then push humidity to 90%.")
            w1, w2, w3, w4 = st.columns(4)
            with w1:
                t_c = st.slider("Temp (°C)", -8.0, 39.0, float(st.session_state["in_t"]), help="20–28°C is the sweet spot.")
            with w2:
                at_c = st.slider("Feels-like (°C)", -16.0, 50.0, float(st.session_state["in_at"]))
            with w3:
                hum_pct = st.slider("Humidity (%)", 0, 100, int(st.session_state["in_hum"]), help="Above 80% demand drops.")
            with w4:
                wind = st.slider("Wind (0–67)", 0, 67, int(st.session_state["in_wind"]), help="Above 30 discourages cycling.")
            st.session_state.update({"in_t": t_c, "in_at": at_c, "in_hum": hum_pct, "in_wind": wind})

    temp, atemp, humidity, windspeed = norm_inputs(t_c, at_c, hum_pct, wind)
    dt = pd.to_datetime(f"{d_str} {h:02d}:00")
    pred = predict_row(dt, season, holiday, workingday, weather, temp, atemp, humidity, windspeed)

    hrs = add_features(pd.DataFrame([{
        "datetime": pd.to_datetime(f"{d_str} {hh:02d}:00"), "season": season, "holiday": holiday,
        "workingday": workingday, "weather": weather, "temp": temp, "atemp": atemp,
        "humidity": humidity, "windspeed": windspeed} for hh in range(24)]))
    hrs["predicted"] = np.expm1(model.predict(hrs[FEATURES])).clip(min=0)
    day_avg = float(hrs["predicted"].mean())
    peak_h = int(hrs["predicted"].idxmax())
    peak_v = float(hrs["predicted"].max())

    st.divider()
    r1, r2 = st.columns([1, 2])
    with r1:
        with st.container(border=True):
            with st.container(border=True):
                eyebrow(f"{DOW[dow_auto]} {dt:%b %d} · {h:02d}:00 · {SEASONS[season]}")
                st.markdown(f'<p class="hero-num">{pred:,}</p>', unsafe_allow_html=True)
                st.caption(f"bikes · {pred - day_avg:+.0f} vs the day average of {day_avg:.0f}")
                show_verdict(pred)
        if tut:
            with st.expander("Explain like I'm five"):
                st.write(f"At **{h}:00 on a {DOW[dow_auto]}** with **{WEATHER[weather]}**, "
                         f"{'commuters' if workingday else 'leisure riders'} need about **{pred} bikes**.")
    with r2:
        with st.container(border=True):
            eyebrow("The full day, same conditions")
            st.line_chart(hrs.set_index(hrs["datetime"].dt.hour)["predicted"], height=260)
            st.caption(f"Day peak {peak_h}:00 — {peak_v:.0f} bikes. "
                       "Workdays show twin commute bumps; flip Working day to No and they vanish.")

# ================= BATCH =================
elif page == "Batch":
    eyebrow("Bulk scoring")
    st.title("Score thousands of hours at once")
    if tut:
        st.info("Download the sample, upload it back, download your predictions. No code needed.")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            eyebrow("01 · Sample")
            try:
                with open("data/test.csv", "rb") as fh:
                    st.download_button("Download test.csv", fh, "test.csv", use_container_width=True)
            except FileNotFoundError:
                st.warning("data/test.csv not found.")
        with c2:
            eyebrow("02 · Upload")
            f = st.file_uploader("CSV with datetime, season, holiday, workingday, weather, temp, atemp, humidity, windspeed",
                                 type=["csv"], label_visibility="collapsed")
    if f is not None:
        bdf = add_features(pd.read_csv(f, parse_dates=["datetime"]))
        preds = np.expm1(model.predict(bdf[FEATURES])).clip(min=0).round().astype(int)
        out = pd.DataFrame({"datetime": bdf["datetime"], "count": preds})
        m1, m2, m3 = st.columns(3)
        m1.metric("Rows scored", f"{len(out):,}")
        m2.metric("Average demand", f"{preds.mean():.0f} bikes")
        m3.metric("Peak hour", f"{preds.max():,}")
        with st.container(border=True):
            st.dataframe(out.head(20), use_container_width=True)
            st.line_chart(out.set_index("datetime")["count"])
            st.download_button("Download submission.csv", out.to_csv(index=False),
                               "submission.csv", use_container_width=True)

# ================= INSIGHTS =================
elif page == "Insights":
    eyebrow("Demand school")
    st.title("What actually moves demand?")
    if tut:
        st.info("Read each card, guess the pattern, then prove it on the Predict page.")
    tr = load_train()
    tr["hour"] = tr["datetime"].dt.hour
    tr["dow"] = tr["datetime"].dt.dayofweek
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            eyebrow("Lesson 01")
            st.subheader("Rush Hours Rule")
            st.bar_chart(tr.groupby("hour")["count"].mean())
            st.caption("Peaks at 8 AM and 5–6 PM. Compare 4 AM against 6 PM in Predict.")
    with c2:
        with st.container(border=True):
            eyebrow("Lesson 02")
            st.subheader("Weekday vs Weekend")
            by_dow = tr.groupby("dow")["count"].mean()
            by_dow.index = [DOW[i] for i in by_dow.index]
            st.bar_chart(by_dow)
            st.caption("Weekends peak midday, never at 8 AM.")
    c3, c4 = st.columns(2)
    with c3:
        with st.container(border=True):
            eyebrow("Lesson 03")
            st.subheader("Weather Penalty")
            st.bar_chart(tr.groupby("weather")["count"].mean())
            st.caption("1 is clear sky, 4 is storm. Feel the drop between them.")
    with c4:
        with st.container(border=True):
            eyebrow("Lesson 04")
            st.subheader("Temperature Sweet Spot")
            st.scatter_chart(tr.sample(min(2000, len(tr)))[["temp", "count"]].set_index("temp"))
            st.caption("Demand climbs to about 20°C, then flattens.")

# ================= ABOUT =================
else:
    eyebrow("Under the hood")
    st.title("How the forecast is made")
    if tut:
        st.info("The model studied 10,886 past hours and learned rules like “5 PM, sunny, workday means busy”.")
    with st.container(border=True):
        eyebrow("Leaderboard")
        st.dataframe(pd.DataFrame([
            {"Model": "Ridge, the baseline", "RMSLE": 1.18},
            {"Model": "RandomForest-100", "RMSLE": 0.71},
            {"Model": "XGBoost, 500 trees", "RMSLE": 0.65},
            {"Model": "HistGradientBoosting, deployed", "RMSLE": 0.53},
        ]), use_container_width=True, hide_index=True)
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            eyebrow("Glossary")
            st.markdown("- **RMSLE** — forecast error. Lower is better.\n"
                        "- **Working day** — a weekday that is not a holiday.\n"
                        "- **Temp scale** — you enter °C; the model sees 0–1.")
    with c2:
        with st.container(border=True):
            eyebrow("Reproduce")
            st.code("pip install -r requirements.txt\npython src/train.py\npython src/predict.py\nstreamlit run app.py", language="bash")

st.divider()
st.caption("BikeShare AI · Capital Bikeshare 2011–2012 · UCI / Kaggle · Streamlit")
