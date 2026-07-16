"""Precompute combined Manufacturer Comparison views for fast Streamlit loading."""
from pathlib import Path
import sys
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.metrics.dashboard_aggregations import prepare_dashboard_views

ROOT=Path(__file__).resolve().parents[1]; SOURCE=ROOT/"data"/"processed"/"manufacturer_comparison_wide.parquet"; OUTPUT=ROOT/"data"/"processed"/"manufacturer_dashboard_views.parquet"
def main():
    result=prepare_dashboard_views(pd.read_parquet(SOURCE)); result.to_parquet(OUTPUT,index=False); print(f"Created {OUTPUT} with {len(result):,} rows")
if __name__=="__main__":main()
