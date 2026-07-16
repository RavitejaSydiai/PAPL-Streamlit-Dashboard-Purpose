"""Build deployable Original Ver Parle SKU productivity dataset."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.data.sku_productivity_data import build_sku_productivity_source
from src.metrics.sku_productivity_metrics import calculate_productivity

ROOT=Path(__file__).resolve().parents[1]; INPUT=ROOT/"data"/"PAPL Phase 1- Transposed File_3_vs.xlsx"; OUT=ROOT/"data"/"processed"/"sku_productivity.parquet"
def main():
    source=build_sku_productivity_source(INPUT); result=calculate_productivity(source); OUT.parent.mkdir(parents=True,exist_ok=True); result.to_parquet(OUT,index=False)
    excluded=len(source)-len(result); audit=f'''# ND–ROS SKU Productivity data preparation

- Sheet: `Original Ver` only
- Period: `Apr 25 - Sep 25`
- Manufacturer: exact source label `PARLE AGRO`
- Exact source facts: `Numeric Distribution Handling (C)` and `Unwghtd ROS (VOL UNIT CASES) Handling (C)`
- State × ITEM × fact duplicate keys: 0
- Aggregation: none; unique observations are pivoted directly
- Source ND scale: percentage points (0 to 69.658); no conversion applied
- Paired valid State × ITEM records: {len(result):,}
- Records excluded after pivot for missing/negative ND or ROS: {excluded:,}
- Bubble display transformation: square root of ND × ROS; original score retained for ranking and hover
- All-state aggregation: not provided because ND and ROS are non-additive across states
'''
    (ROOT/"docs"/"sku_productivity_audit.md").write_text(audit,encoding="utf-8"); print(f"Created {OUT} with {len(result):,} records; excluded {excluded:,}")
if __name__=="__main__": main()
