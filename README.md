# Smart Factory Digital Twin

A Streamlit dashboard prototype for a manufacturing assembly line. It includes
production analytics, equipment status, synthetic predictive-maintenance
indicators, and an interactive 3D assembly model.

[Live demo](https://smart-factory-digital-twin.streamlit.app/)

The public demo creates a local SQLite database with synthetic sample history
when it starts. It is read-only from the dashboard and is not connected to real
factory equipment. The sample database is regenerated after a fresh deployment
or restart; it is not a persistent data store.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Deployment

This repository is deployed on
[Streamlit Community Cloud](https://share.streamlit.io/) from the `main` branch,
using `app.py` as the entry point. To redeploy or manage it, open Streamlit
Community Cloud and select the `Kavin-123-crea/smart-factory-digital`
repository.

The `.gitignore` excludes local virtual environments, the SQLite database,
generated model files, presentation exports, and STEP CAD files. The hosted app
uses only synthetic data created at startup.

## Limitations

- The dashboard refreshes its display, but this prototype does not connect to
  live machinery or run the separate `simulator.py` process in the cloud.
- Predictive-maintenance values are illustrative and are not validated for
  industrial use.
