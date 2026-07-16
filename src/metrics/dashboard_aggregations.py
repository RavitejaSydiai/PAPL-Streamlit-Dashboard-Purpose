"""Documented combined-state/category views for Manufacturer Comparison."""
from pathlib import Path
import sys
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from config.fact_aggregation_rules import FACT_RULES

SALES="Sales Value (000)"
CATEGORY_MAP={"PACKAGED PLAIN WATER":"PDW","RTD MIXERS":"PDW","MANGO DRINKS":"MANGO DRINKS","MILK DRINKS":"MILK DRINKS","RTD SUGAR":"RTD SUGAR"}

def _weighted(group,column):
    valid=group[column].notna(); weights=group.loc[valid,SALES].fillna(0) if SALES in group else pd.Series(dtype=float)
    if valid.any() and weights.sum()>0:return float((group.loc[valid,column]*weights).sum()/weights.sum())
    return float(group.loc[valid,column].mean()) if valid.any() else pd.NA

def _aggregate(group,state,category,coverage_mode="max"):
    row={"State":state,"S4CATEGORY":category,"Manufacturer":group.Manufacturer.iloc[0]}
    for column in [c for c in group.columns if c not in ["State","S4CATEGORY","Manufacturer"]]:
        rule=FACT_RULES.get(column)
        if rule is None:continue
        if rule["class"] in ["additive","snapshot"]: row[column]=group[column].sum(min_count=1)
        elif rule["class"]=="coverage": row[column]=group[column].sum(min_count=1) if coverage_mode=="sum" else group[column].max()
        else: row[column]=_weighted(group,column)
    return row

def prepare_dashboard_views(wide:pd.DataFrame)->pd.DataFrame:
    base=wide[wide.S4CATEGORY.isin(CATEGORY_MAP)].copy(); base["S4CATEGORY"]=base.S4CATEGORY.map(CATEGORY_MAP)
    state_category=[]
    for (state,category,manufacturer),g in base.groupby(["State","S4CATEGORY","Manufacturer"],sort=False): state_category.append(_aggregate(g,state,category,"max"))
    scoped=pd.DataFrame(state_category)
    nartd=[]
    for (state,manufacturer),g in scoped.groupby(["State","Manufacturer"],sort=False): nartd.append(_aggregate(g,state,"NARTD","max"))
    scoped=pd.concat([scoped,pd.DataFrame(nartd)],ignore_index=True)
    all_india=[]
    for (category,manufacturer),g in scoped.groupby(["S4CATEGORY","Manufacturer"],sort=False): all_india.append(_aggregate(g,"ALL INDIA",category,"sum"))
    return pd.concat([scoped,pd.DataFrame(all_india)],ignore_index=True)
