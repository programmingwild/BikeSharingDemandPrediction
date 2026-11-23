# Metro Demand Studio — new UI

This is a **separate** UI. `streamlit_app.py` is left untouched.

- `app_v2.py` — the new app entrypoint (Streamlit is the backend: it loads
  `src/model.pkl`, runs predictions and serves the page).
- `ui_v2.py` — its independent design system (HTML/CSS only, no new packages).

## Run locally

```bash
pip install -r requirements.txt
streamlit run app_v2.py
```

## Deploy on Streamlit Community Cloud

The GitHub repo already has a deployed Streamlit app. To deploy this UI instead
without deleting the old one:

1. Open your app in Streamlit Community Cloud → **Manage app**.
2. Go to **Settings → Main file path** and change it from
   `streamlit_app.py` to `app_v2.py`.
3. Save. Streamlit rebuilds and serves the new UI.

To go back, set the main file path back to `streamlit_app.py`.

## What is different

- Warm editorial paper theme with Fraunces display type (completely different
  from the original Streamlit look).
- Top navigation instead of a sidebar.
- Live forecast hero with a 24-hour bar field generated from model output.
- Week heatmap: 7 days × 24 hours, 168 live predictions.
- Weather sensitivity comparison and a plain-language fleet note.
- Batch scoring, data insights and model leaderboard.
