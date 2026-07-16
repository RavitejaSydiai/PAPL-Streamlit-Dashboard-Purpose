import pandas as pd
from src.metrics.manufacturer_metrics import build_comparison

def test_rank_and_leader():
    d=pd.DataFrame([{"State":"X","S4CATEGORY":"C","Manufacturer":"PARLE AGRO","Fact":"Sales Value (000)","Metric_Value":80,"Observation_Count":1,"Aggregation":"sum","Fact_Class":"additive"},{"State":"X","S4CATEGORY":"C","Manufacturer":"LEADER","Fact":"Sales Value (000)","Metric_Value":100,"Observation_Count":1,"Aggregation":"sum","Fact_Class":"additive"}])
    r=build_comparison(d); p=r[r.Manufacturer.eq("PARLE AGRO")].iloc[0]
    assert p.Manufacturer_Rank==2 and p.Market_Leader=="LEADER" and p.Gap_to_Leader==20

def test_near_parity():
    d=pd.DataFrame([{"State":"X","S4CATEGORY":"C","Manufacturer":"PARLE AGRO","Fact":"Sales Value (000)","Metric_Value":98,"Observation_Count":1,"Aggregation":"sum","Fact_Class":"additive"},{"State":"X","S4CATEGORY":"C","Manufacturer":"A","Fact":"Sales Value (000)","Metric_Value":100,"Observation_Count":1,"Aggregation":"sum","Fact_Class":"additive"}])
    r=build_comparison(d); assert r[r.Manufacturer.eq("A")].iloc[0].Comparison_Status=="Near Parity"
