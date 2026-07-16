# ND–ROS SKU Productivity data preparation

- Sheet: `Original Ver` only
- Period: `Apr 25 - Sep 25`
- Manufacturer: exact source label `PARLE AGRO`
- Exact source facts: `Numeric Distribution Handling (C)` and `Unwghtd ROS (VOL UNIT CASES) Handling (C)`
- State × ITEM × fact duplicate keys: 0
- Aggregation: none; unique observations are pivoted directly
- Source ND scale: percentage points (0 to 69.658); no conversion applied
- Paired valid State × ITEM records: 951
- Records excluded after pivot for missing/negative ND or ROS: 41
- Bubble display transformation: square root of ND × ROS; original score retained for ranking and hover
- All-state aggregation: not provided because ND and ROS are non-additive across states
