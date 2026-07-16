"""Build all Original Ver manufacturer benchmarking outputs."""
from __future__ import annotations
import json
from pathlib import Path
import sys
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from config.fact_aggregation_rules import FACT_RULES,PARLE_MANUFACTURER_NAME,NEAR_PARITY_TOLERANCE
from src.data.original_ver_loader import load_original_comparison
from src.metrics.manufacturer_metrics import build_comparison,build_wide
from src.insights.comparison_insight_engine import diagnose_group
from src.charts.manufacturer_charts import build_suite,save_suite

ROOT=Path(__file__).resolve().parents[1]; INPUT=ROOT/"data"/"PAPL Phase 1- Transposed File_3_vs.xlsx"; PROCESSED=ROOT/"data"/"processed"; DOCS=ROOT/"docs"; CHARTS=DOCS/"manufacturer_charts"

def main(write_images=False):
    PROCESSED.mkdir(parents=True,exist_ok=True); DOCS.mkdir(exist_ok=True)
    print("Loading and aggregating Original Ver...",flush=True)
    named,blank=load_original_comparison(INPUT)
    comparison=build_comparison(named); wide=build_wide(comparison)
    comparison.to_parquet(PROCESSED/"manufacturer_comparison_long.parquet",index=False)
    wide.to_parquet(PROCESSED/"manufacturer_comparison_wide.parquet",index=False)
    blank.to_parquet(PROCESSED/"category_total_benchmarks.parquet",index=False)
    insight_rows=[]
    for (state,category),group in wide.groupby(["State","S4CATEGORY"]):
        result=diagnose_group(group); result.update({"State":state,"S4CATEGORY":category}); insight_rows.append(result)
    insights=pd.DataFrame(insight_rows)
    insights.to_json(PROCESSED/"executive_comparison_insights.json",orient="records",indent=2)
    insights[["State","S4CATEGORY","Parle_Rank","Leader","Parle_Value","Leader_Value","Gap","Diagnosis","Recommendation"]].to_csv(PROCESSED/"parle_opportunity_by_state_category.csv",index=False)
    state="Maharashtra" if "Maharashtra" in wide.State.values else wide.State.dropna().iloc[0]
    category="MANGO DRINKS" if "MANGO DRINKS" in wide.S4CATEGORY.values else wide.S4CATEGORY.iloc[0]
    figs=build_suite(wide,insights,state,category); items=save_suite(figs,CHARTS,write_images=write_images)
    catalogue=["# Metric catalogue","","All rules apply only to `Original Ver`. No valid row-level weights exist for ratios/rates, so documented means are used.",""]
    for fact,rule in FACT_RULES.items(): catalogue += [f"## {fact}",f"- Class: {rule['class']}",f"- Aggregation: `{rule['aggregation']}`",f"- Higher is better: `{rule['higher_is_better']}`",""]
    (DOCS/"metric_catalogue.md").write_text("\n".join(catalogue),encoding="utf-8")
    findings=["# Manufacturer comparison findings","",f"- Source sheet: `Original Ver` only",f"- Exact Parle label: `{PARLE_MANUFACTURER_NAME}`",f"- Near-parity tolerance: ±{NEAR_PARITY_TOLERANCE*100:.0f}%",f"- Named fact rows after aggregation: {len(named):,}",f"- Blank-manufacturer benchmarks kept separate: {len(blank):,}",f"- State × S4CATEGORY insights: {len(insights):,}","","## Evidence-led findings",""]
    for _,r in insights.sort_values(["Parle_Rank","Gap"]).iterrows(): findings += [f"### {r.State} · {r.S4CATEGORY}",r.Insight,""]
    findings += ["## Limitations","","- The workbook has no Facts column; facts are separate columns.","- CATEGORY, SEGMENT, SUBSEGMENT, BRAND and SUBBRAND are absent.","- Ratio/rate means are unweighted because a valid weighting field at the repeated-row grain is unavailable.","- Blank-manufacturer rows are excluded from manufacturer rankings and stored separately as category benchmarks."]
    (DOCS/"manufacturer_comparison_findings.md").write_text("\n".join(findings),encoding="utf-8")
    print(f"Built {len(items)} charts, {len(insights)} insights and processed Parquet outputs.")

if __name__=="__main__": main("--images" in sys.argv)
