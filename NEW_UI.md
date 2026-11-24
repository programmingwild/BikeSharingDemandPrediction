# BikeShare Demand Studio

The live Streamlit app is `streamlit_app.py`. It is **self-contained**: both the
design system and the UI live in that one file, so Streamlit Cloud runs it
directly with no fragile local-module imports.

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy

Push to `main`. Streamlit Community Cloud rebuilds automatically from
`streamlit_app.py` and serves the new UI at the existing app URL.

Pages can be deep-linked: `?page=Forecast`, `?page=Batch`, `?page=Insights`,
`?page=About`.

## Notes

- Model and feature code stay in `src/`; training extras are in
  `requirements-dev.txt`.
- The UI uses only Streamlit plus the pinned requirements — no new packages.
