# PAPL Streamlit Manufacturer Benchmarking Dashboard

Interactive commercial-intelligence dashboard comparing Parle Agro with named manufacturers across states and S4 categories.

## Run locally

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Streamlit Community Cloud

- Entry point: `app.py`
- Python dependencies: `requirements.txt`
- Runtime data: `data/processed/`

The deployed dashboard uses processed Parquet/JSON outputs. Raw Excel workbooks and backup files are intentionally excluded from Git.
