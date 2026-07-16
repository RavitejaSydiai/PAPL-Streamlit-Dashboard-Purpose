"""Manufacturer ranks and Parle-versus-leader metrics."""

from __future__ import annotations

from pathlib import Path
import sys
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from config.fact_aggregation_rules import FACT_RULES, NEAR_PARITY_TOLERANCE, PARLE_MANUFACTURER_NAME


def build_comparison(named: pd.DataFrame) -> pd.DataFrame:
    pieces = []
    for (state, category, fact), group in named.groupby(["State", "S4CATEGORY", "Fact"], sort=False):
        g = group.copy()
        higher = FACT_RULES[fact]["higher_is_better"]
        ascending = higher is False
        g["Manufacturer_Rank"] = g["Metric_Value"].rank(method="min", ascending=ascending).astype(int)
        leader = g.sort_values("Metric_Value", ascending=ascending).iloc[0]
        parle_rows = g[g["Manufacturer"].eq(PARLE_MANUFACTURER_NAME)]
        parle_value = float(parle_rows.iloc[0]["Metric_Value"]) if not parle_rows.empty else None
        g["Market_Leader"] = leader["Manufacturer"]
        g["Leader_Value"] = float(leader["Metric_Value"])
        g["Gap_to_Leader"] = (g["Leader_Value"] - g["Metric_Value"]).abs()
        g["Gap_to_Leader_Percent"] = g["Gap_to_Leader"] / g["Leader_Value"].abs().replace(0, pd.NA) * 100
        g["Parle_Value"] = parle_value
        g["Competitor_Value"] = g["Metric_Value"]
        g["Difference_vs_Parle"] = g["Metric_Value"] - parle_value if parle_value is not None else pd.NA
        if parle_value is None:
            g["Comparison_Status"] = "Insufficient Data"
        else:
            tolerance = max(abs(parle_value), 1e-12) * NEAR_PARITY_TOLERANCE
            g["Comparison_Status"] = g["Difference_vs_Parle"].apply(lambda d: "Near Parity" if abs(d) <= tolerance else "Parle Trails" if d > 0 else "Parle Leads")
            g.loc[g["Manufacturer"].eq(PARLE_MANUFACTURER_NAME), "Comparison_Status"] = "Parle Leads" if leader["Manufacturer"] == PARLE_MANUFACTURER_NAME else "Parle Trails"
        pieces.append(g)
    return pd.concat(pieces, ignore_index=True) if pieces else pd.DataFrame()


def build_wide(comparison: pd.DataFrame) -> pd.DataFrame:
    return comparison.pivot_table(index=["State", "S4CATEGORY", "Manufacturer"], columns="Fact", values="Metric_Value", aggfunc="first").reset_index()
