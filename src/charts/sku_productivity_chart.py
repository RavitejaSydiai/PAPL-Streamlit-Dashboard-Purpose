"""Interactive Plotly ND–ROS SKU Productivity Matrix."""
import pandas as pd
import plotly.express as px

COLORS={"Core Winners":"#2E7D32","Distribution Expansion Opportunity":"#F5A623","Productivity Improvement Required":"#D95F02","Review / Low Priority":"#9E9E9E"}
def create_sku_productivity_chart(data:pd.DataFrame,state:str,top_n:int|None=20):
    d=data[data.State.eq(state)].sort_values("ND_ROS_Score",ascending=False).copy()
    if top_n is not None:d=d.head(top_n)
    median_nd=float(data.loc[data.State.eq(state),"Numeric_Distribution"].median()); median_ros=float(data.loc[data.State.eq(state),"Unweighted_ROS"].median())
    fig=px.scatter(d,x="Numeric_Distribution",y="Unweighted_ROS",size="Bubble_Size_Display",color="ITEM",hover_name="ITEM",custom_data=["State","ITEM","Numeric_Distribution","Unweighted_ROS","ND_ROS_Score","Rank","Quadrant"],size_max=55,template="plotly_white")
    fig.update_traces(opacity=.74,marker=dict(line=dict(width=1,color="white")),hovertemplate="State: %{customdata[0]}<br>ITEM: %{customdata[1]}<br>Numeric Distribution: %{customdata[2]:.2f}%<br>Unweighted ROS: %{customdata[3]:.3f}<br>ND × ROS Score: %{customdata[4]:,.2f}<br>SKU Rank: %{customdata[5]}<br>Quadrant: %{customdata[6]}<extra></extra>")
    fig.add_vline(x=median_nd,line_dash="dash",line_color="#555"); fig.add_hline(y=median_ros,line_dash="dash",line_color="#555")
    xmax=max(float(d.Numeric_Distribution.max()),median_nd)*1.08 if not d.empty else 1; ymax=max(float(d.Unweighted_ROS.max()),median_ros)*1.08 if not d.empty else 1
    labels=[(median_nd+(xmax-median_nd)*.5,median_ros+(ymax-median_ros)*.9,"Core Winners"),(median_nd*.5,median_ros+(ymax-median_ros)*.9,"Distribution Expansion Opportunity"),(median_nd+(xmax-median_nd)*.5,median_ros*.12,"Productivity Improvement Required"),(median_nd*.5,median_ros*.12,"Review / Low Priority")]
    for x,y,t in labels: fig.add_annotation(x=x,y=y,text=t,showarrow=False,font=dict(size=10,color="#666"),bgcolor="rgba(255,255,255,.65)")
    fig.update_layout(title=f"ND–ROS SKU Productivity Matrix — {state}",xaxis_title="Numeric Distribution Handling (C) (%)",yaxis_title="Unweighted ROS (Volume Unit Cases)",height=720,legend_title="ITEM / SKU",showlegend=top_n is not None,margin=dict(l=70,r=40,t=85,b=70),modebar_add=["toImage"])
    return fig
