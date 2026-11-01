# Smart Factory Digital Twin

A Streamlit dashboard prototype for a manufacturing assembly line. It includes
production analytics, equipment status, synthetic predictive-maintenance
indicators, and an interactive 3D assembly model.

[Live demo](https://smart-factory-digital-twin.streamlit.app/)

The public demo creates a local SQLite database with synthetic sample history
when it starts and appends simulated readings as the dashboard refreshes. It is
not connected to real factory equipment. The maintenance button starts a
30-second simulated maintenance interval shared by visitors; it preserves
production history and restores simulated machine health. The separate Reset
Factory Data button resets production to zero, clears shared charts and logs,
and returns the simulated readings to a fresh baseline. The sample database is
regenerated after a fresh deployment or restart; it is not persistent.

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
uses only synthetic data created at startup and during dashboard refreshes.

## Limitations

- The displayed readings are simulated, not live machinery data; the hosted
  app does not run the separate `simulator.py` process.
- Predictive-maintenance values are illustrative and are not validated for
  industrial use.
