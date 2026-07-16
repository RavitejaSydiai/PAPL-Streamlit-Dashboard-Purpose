"""Audited aggregation rules for facts in Original Ver."""

PARLE_MANUFACTURER_NAME = "PARLE AGRO"
NEAR_PARITY_TOLERANCE = 0.05

FACT_RULES = {
    "Sales Value (000)": {"class": "additive", "aggregation": "sum", "higher_is_better": True},
    "Sales (VOL UNIT CASES)": {"class": "additive", "aggregation": "sum", "higher_is_better": True},
    "Sales Units": {"class": "additive", "aggregation": "sum", "higher_is_better": True},
    "Sales (Vol (KG/LT/000NO))": {"class": "additive", "aggregation": "sum", "higher_is_better": True},
    "Purchase (VOL UNIT CASES)": {"class": "additive", "aggregation": "sum", "higher_is_better": True},
    "Share of Sales Value - Product": {"class": "ratio", "aggregation": "mean", "higher_is_better": True},
    "Share of Sales - Sales (VOL UNIT CASES) - Product": {"class": "ratio", "aggregation": "mean", "higher_is_better": True},
    "Share of Sales - Sales Units - Product": {"class": "ratio", "aggregation": "mean", "higher_is_better": True},
    "Stocks (VOL UNIT CASES) Shr - Product": {"class": "ratio", "aggregation": "mean", "higher_is_better": True},
    "Purchase (VOL UNIT CASES) Shr - Product": {"class": "ratio", "aggregation": "mean", "higher_is_better": True},
    "Numeric Distribution Handling (C)": {"class": "ratio", "aggregation": "mean", "higher_is_better": True},
    "Numeric Out of Stock (C)": {"class": "ratio", "aggregation": "mean", "higher_is_better": False},
    "Wghtd Dist Out of Stock": {"class": "ratio", "aggregation": "mean", "higher_is_better": False},
    "Relative Numeric Distribution Handling (C) - Product": {"class": "ratio", "aggregation": "mean", "higher_is_better": True},
    "Value Shr in Handlers (C) - Product - CATEGORY": {"class": "ratio", "aggregation": "mean", "higher_is_better": True},
    "Wghtd Dist Handling (C) - CATEGORY": {"class": "ratio", "aggregation": "mean", "higher_is_better": True},
    "Price per Sales (VOL UNIT CASES)": {"class": "rate", "aggregation": "mean", "higher_is_better": None},
    "Sales (VOL UNIT CASES) Price Index - Product": {"class": "ratio", "aggregation": "mean", "higher_is_better": None},
    "Price per Sales Unit": {"class": "rate", "aggregation": "mean", "higher_is_better": None},
    "Unwghtd ROS (VOL UNIT CASES) Handling (C)": {"class": "rate", "aggregation": "mean", "higher_is_better": True},
    "Days of Supply (Vol (KG/LT/000NO))": {"class": "rate", "aggregation": "mean", "higher_is_better": None},
    "Stocks Forward (VOL UNIT CASES)": {"class": "snapshot", "aggregation": "max", "higher_is_better": True},
    "Stocks Backward (VOL UNIT CASES)": {"class": "snapshot", "aggregation": "max", "higher_is_better": True},
    "Stocks (VOL UNIT CASES)": {"class": "snapshot", "aggregation": "max", "higher_is_better": True},
    "Number of Stores Retailing (C)": {"class": "coverage", "aggregation": "max", "higher_is_better": True},
}
