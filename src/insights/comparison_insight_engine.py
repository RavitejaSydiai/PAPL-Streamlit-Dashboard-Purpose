"""Evidence-led State × S4CATEGORY insights for Parle Agro."""

from __future__ import annotations
import pandas as pd
from .comparison_rules import *


def _metric(wide, manufacturer, metric):
    row = wide[wide["Manufacturer"].eq(manufacturer)]
    if row.empty or metric not in row or pd.isna(row.iloc[0][metric]): return None
    return float(row.iloc[0][metric])


def diagnose_group(group: pd.DataFrame) -> dict:
    sales = group.dropna(subset=[SALES]).sort_values(SALES, ascending=False) if SALES in group else pd.DataFrame()
    parle = group[group["Manufacturer"].eq(PARLE)]
    if sales.empty or parle.empty or pd.isna(parle.iloc[0].get(SALES)):
        return {"Diagnosis":"Insufficient Evidence","Recommendation":"Insufficient evidence","Triggered_Metrics":[],"Insight":"Insufficient evidence to determine the primary performance driver."}
    leader = sales.iloc[0]
    pv, lv = float(parle.iloc[0][SALES]), float(leader[SALES])
    rank = int(sales[SALES].rank(method="min", ascending=False).loc[parle.index[0]])
    ndp, ndl = _metric(parle, PARLE, ND), _metric(sales, leader["Manufacturer"], ND)
    rosp, rosl = _metric(parle, PARLE, ROS), _metric(sales, leader["Manufacturer"], ROS)
    oosp, oosl = _metric(parle, PARLE, OOS), _metric(sales, leader["Manufacturer"], OOS)
    storesp, storesl = _metric(parle, PARLE, STORES), _metric(sales, leader["Manufacturer"], STORES)
    pricep, pricel = _metric(parle, PARLE, PRICE), _metric(sales, leader["Manufacturer"], PRICE)
    triggered=[]
    if leader["Manufacturer"] == PARLE:
        diagnosis, recommendation = "Market Leader", "Defend market leadership"; triggered=[SALES]
    elif lv and abs(lv-pv)/abs(lv) <= .05:
        diagnosis, recommendation = "Balanced / Near Parity", "Maintain current position"; triggered=[SALES]
    elif ndp is not None and ndl is not None and rosp is not None and rosl is not None and ndl-ndp>10 and rosp>=.95*rosl:
        diagnosis, recommendation = "Strong Productivity, Low Distribution", "Expand numeric distribution"; triggered=[ND,ROS]
    elif ndp is not None and ndl and rosp is not None and rosl and ndp>=.9*ndl and rosp<.8*rosl:
        diagnosis, recommendation = "High Distribution, Low Productivity", "Improve rate of sale"; triggered=[ND,ROS]
    elif oosp is not None and oosl is not None and oosp-oosl>2:
        diagnosis, recommendation = "Availability / Out-of-Stock Risk", "Correct out-of-stock issues"; triggered=[OOS]
    elif storesp is not None and storesl and storesp<.8*storesl:
        diagnosis, recommendation = "Store Coverage Gap", "Expand numeric distribution"; triggered=[STORES]
    elif pricep is not None and pricel and pricep>1.1*pricel:
        diagnosis, recommendation = "Price Premium", "Review price positioning"; triggered=[PRICE]
    elif rosp is not None and rosl and rosp<.8*rosl:
        diagnosis, recommendation = "Weak Consumer Offtake", "Improve rate of sale"; triggered=[ROS]
    else:
        diagnosis, recommendation = "Insufficient Evidence", "Insufficient evidence"; triggered=[]
    gap=lv-pv
    evidence=f"Parle ranks {rank} by Sales Value at {pv:,.2f}; {leader['Manufacturer']} leads at {lv:,.2f}, a gap of {gap:,.2f} ({gap/lv*100:.1f}% of leader value)."
    insight=f"{evidence} Primary diagnosis: {diagnosis}. Recommended action: {recommendation}. This uses Apr–Sep 2025 aggregated retail-audit data and does not establish causality."
    return {"Diagnosis":diagnosis,"Recommendation":recommendation,"Triggered_Metrics":triggered,"Insight":insight,"Parle_Rank":rank,"Parle_Value":pv,"Leader":leader["Manufacturer"],"Leader_Value":lv,"Gap":gap}
