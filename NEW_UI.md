# BikeShare Demand Studio

The redesigned UI is in `app_v2.py` with its design system in `ui_v2.py`.
`streamlit_app.py` is the live entrypoint and simply imports `app_v2.py`, so
Streamlit Community Cloud serves the new UI at the existing app URL.

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py     # or: streamlit run app_v2.py
```

## Deploy

Push to `main`. Streamlit Cloud rebuilds from `streamlit_app.py` automatically.
No dashboard setting changes are needed.

Pages can also be deep-linked: `?page=Forecast`, `?page=Batch`,
`?page=Insights`, `?page=About`.

## What changed

- Stores the full UI in `app_v2.py` / `ui_v2.py`, leaving the model and data
  code (`src/`, `data/`) untouched.
- Dark/light theme-safe editorial paper design with Fraunces display type,
  bento cards, sticky results panel and a live bottom-right readout.
- Live hourly forecast, 7×24 heatmap, weather sensitivity, fleet note,
  batch scoring, data insights and leaderboard.
