# Smart Factory Digital Twin

A Streamlit dashboard prototype for a manufacturing assembly line. It includes
production analytics, equipment status, synthetic predictive-maintenance
indicators, and an interactive 3D assembly model.

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

## Deploy to Streamlit Community Cloud

1. Sign in to GitHub and create an empty **public** repository.
2. From this project directory, push the source and required assets:

   ```powershell
   git init -b main
   git add .
   git commit -m "Initial project upload"
   git remote add origin https://github.com/<YOUR_USERNAME>/<REPOSITORY>.git
   git push -u origin main
   ```

   Include `app.py`, `requirements.txt`, `README.md`, and the `images`
   directory (the OBJ/MTL files power the 3D view). The `.gitignore` keeps
   local databases, model binaries, presentation exports, and virtual
   environments out of the public repository.
3. In [Streamlit Community Cloud](https://share.streamlit.io/), connect the
   GitHub repository and deploy `app.py` from the `main` branch.
4. The app URL is assigned by Streamlit Community Cloud after deployment.

The `.gitignore` excludes local virtual environments, the SQLite database,
generated model files, presentation exports, and STEP CAD files. The hosted app
uses only synthetic data created at startup.

## Limitations

- The dashboard refreshes its display, but this prototype does not connect to
  live machinery or run the separate `simulator.py` process in the cloud.
- Predictive-maintenance values are illustrative and are not validated for
  industrial use.
