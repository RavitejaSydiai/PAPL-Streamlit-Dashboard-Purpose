import pandas as pd
from src.metrics.sku_productivity_metrics import calculate_productivity

def sample():
    return pd.DataFrame([{"State":"A","ITEM":"Winner","Numeric_Distribution":20.0,"Unweighted_ROS":5.0},{"State":"A","ITEM":"Opportunity","Numeric_Distribution":5.0,"Unweighted_ROS":6.0},{"State":"A","ITEM":"Concern","Numeric_Distribution":25.0,"Unweighted_ROS":1.0},{"State":"A","ITEM":"Missing","Numeric_Distribution":None,"Unweighted_ROS":3.0}])
def test_score_and_ranking():
    d=calculate_productivity(sample()); w=d[d.ITEM.eq("Winner")].iloc[0]; assert w.ND_ROS_Score==100 and w.Rank==1
def test_missing_excluded(): assert "Missing" not in calculate_productivity(sample()).ITEM.tolist()
def test_state_filtering():
    d=sample(); d.loc[len(d)]={"State":"B","ITEM":"B1","Numeric_Distribution":10,"Unweighted_ROS":2}; r=calculate_productivity(d); assert len(r[r.State.eq("B")])==1
def test_quadrant_assignment():
    d=calculate_productivity(sample()); assert d[d.ITEM.eq("Opportunity")].iloc[0].Quadrant=="Distribution Expansion Opportunity"
def test_negative_excluded():
    d=sample(); d.loc[len(d)]={"State":"A","ITEM":"Negative","Numeric_Distribution":-1,"Unweighted_ROS":2}; assert "Negative" not in calculate_productivity(d).ITEM.tolist()
