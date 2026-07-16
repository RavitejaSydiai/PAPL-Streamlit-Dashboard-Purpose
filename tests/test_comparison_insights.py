import pandas as pd
from src.insights.comparison_insight_engine import diagnose_group
from src.insights.comparison_rules import SALES,ND,ROS

def test_market_leader():
    d=pd.DataFrame([{"Manufacturer":"PARLE AGRO",SALES:100,ND:20,ROS:5},{"Manufacturer":"A",SALES:90,ND:30,ROS:4}])
    assert diagnose_group(d)["Diagnosis"]=="Market Leader"

def test_low_distribution_strong_productivity():
    d=pd.DataFrame([{"Manufacturer":"PARLE AGRO",SALES:80,ND:20,ROS:10},{"Manufacturer":"A",SALES:100,ND:40,ROS:10}])
    assert diagnose_group(d)["Diagnosis"]=="Strong Productivity, Low Distribution"

def test_missing_data():
    d=pd.DataFrame([{"Manufacturer":"A",SALES:100}]); assert diagnose_group(d)["Diagnosis"]=="Insufficient Evidence"
