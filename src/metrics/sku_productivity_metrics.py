"""Scores, ranks, and median-quadrant assignments for SKU productivity."""
import numpy as np
import pandas as pd

def calculate_productivity(data:pd.DataFrame)->pd.DataFrame:
    d=data.copy(); d=d.dropna(subset=["State","ITEM","Numeric_Distribution","Unweighted_ROS"]); d=d[(d.Numeric_Distribution>=0)&(d.Unweighted_ROS>=0)].copy()
    d["ND_ROS_Score"]=d.Numeric_Distribution*d.Unweighted_ROS
    d["Bubble_Size_Display"]=np.sqrt(d.ND_ROS_Score.clip(lower=0))
    d["Median_ND"]=d.groupby("State").Numeric_Distribution.transform("median"); d["Median_ROS"]=d.groupby("State").Unweighted_ROS.transform("median")
    high_nd=d.Numeric_Distribution>=d.Median_ND; high_ros=d.Unweighted_ROS>=d.Median_ROS
    d["Quadrant"]=np.select([high_nd&high_ros,~high_nd&high_ros,high_nd&~high_ros],["Core Winners","Distribution Expansion Opportunity","Productivity Improvement Required"],default="Review / Low Priority")
    d["Rank"]=d.groupby("State").ND_ROS_Score.rank(method="min",ascending=False).astype(int)
    return d.sort_values(["State","Rank","ITEM"]).reset_index(drop=True)

def state_summary(data:pd.DataFrame,state:str)->dict:
    d=data[data.State.eq(state)].sort_values("Rank");
    if d.empty:return {}
    best=d.iloc[0]; high_nd=d.loc[d.Numeric_Distribution.idxmax()]; high_ros=d.loc[d.Unweighted_ROS.idxmax()]
    counts=d.Quadrant.value_counts().to_dict(); opportunities=d[d.Quadrant.eq("Distribution Expansion Opportunity")].nlargest(3,"ND_ROS_Score"); concerns=d[d.Quadrant.eq("Productivity Improvement Required")].nlargest(3,"Numeric_Distribution")
    return {"Highest_Score_SKU":best.ITEM,"Highest_Score":best.ND_ROS_Score,"Highest_ND_SKU":high_nd.ITEM,"Highest_ND":high_nd.Numeric_Distribution,"Highest_ROS_SKU":high_ros.ITEM,"Highest_ROS":high_ros.Unweighted_ROS,"Quadrant_Counts":counts,"Distribution_Opportunities":opportunities.ITEM.tolist(),"Productivity_Concerns":concerns.ITEM.tolist()}
