"""Transparent rule definitions for Parle performance diagnosis."""

PARLE = "PARLE AGRO"
SALES = "Sales Value (000)"
SHARE = "Share of Sales Value - Product"
ND = "Numeric Distribution Handling (C)"
WD = "Wghtd Dist Handling (C) - CATEGORY"
ROS = "Unwghtd ROS (VOL UNIT CASES) Handling (C)"
STORES = "Number of Stores Retailing (C)"
OOS = "Numeric Out of Stock (C)"
PRICE = "Price per Sales Unit"
STOCK = "Stocks (VOL UNIT CASES)"

RULE_DESCRIPTIONS = {
    "Market Leader": "Parle ranks first by Sales Value.",
    "Strong Productivity, Low Distribution": "Parle ND trails the leader by >10pp while ROS is at least 95% of leader ROS.",
    "High Distribution, Low Productivity": "Parle ND is at least 90% of leader ND while ROS is below 80% of leader ROS.",
    "Availability / Out-of-Stock Risk": "Parle OOS exceeds leader OOS by >2pp.",
    "Store Coverage Gap": "Parle store coverage is below 80% of leader coverage.",
    "Price Premium": "Parle price per unit is >10% above the leader.",
    "Balanced / Near Parity": "Parle Sales Value is within 5% of the leader.",
    "Weak Consumer Offtake": "Parle ROS is below 80% of the leader.",
    "Insufficient Evidence": "Required metrics are unavailable.",
}
