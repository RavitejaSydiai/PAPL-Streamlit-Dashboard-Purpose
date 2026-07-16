"""Streamlit ND–ROS SKU Productivity page."""
from pathlib import Path
import sys
import streamlit as st
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.data.sku_productivity_data import load_processed
from src.metrics.sku_productivity_metrics import state_summary
from src.charts.sku_productivity_chart import create_sku_productivity_chart

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/"data"/"processed"/"sku_productivity.parquet"
st.set_page_config(page_title="SKU Productivity",layout="wide"); st.title("ND–ROS SKU Productivity Matrix"); st.caption("PARLE AGRO · Original Ver · Apr–Sep 2025")
d=load_processed(DATA); states=sorted(d.State.dropna().unique()); state=st.selectbox("State",states,index=0); option=st.selectbox("SKUs shown",["Top 10","Top 20","Top 30","All SKUs"],index=1); top_n=None if option=="All SKUs" else int(option.split()[-1])
fig=create_sku_productivity_chart(d,state,top_n); st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":True,"displaylogo":False})
s=state_summary(d,state); st.subheader("Deterministic insight summary")
if s:
    st.write(f"**{s['Highest_Score_SKU']}** has the highest combined ND–ROS score ({s['Highest_Score']:,.2f}).")
    st.write(f"Highest Numeric Distribution: **{s['Highest_ND_SKU']}** ({s['Highest_ND']:.2f}%). Highest ROS: **{s['Highest_ROS_SKU']}** ({s['Highest_ROS']:.3f}).")
    st.write("Quadrant counts: "+", ".join(f"{k}: {v}" for k,v in s['Quadrant_Counts'].items())+".")
    st.write("Top distribution-expansion candidates: "+(", ".join(s['Distribution_Opportunities']) or "None")+".")
    st.write("Top productivity concerns: "+(", ".join(s['Productivity_Concerns']) or "None")+".")
table=d[d.State.eq(state)][["Rank","ITEM","Numeric_Distribution","Unweighted_ROS","ND_ROS_Score","Quadrant"]].sort_values("Rank")
st.subheader("State SKU table"); st.dataframe(table,use_container_width=True,hide_index=True); st.download_button("Download state table as CSV",table.to_csv(index=False),f"{state}_sku_productivity.csv","text/csv")
