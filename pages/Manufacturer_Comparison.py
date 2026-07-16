"""Streamlit manufacturer benchmarking page using Original Ver outputs only."""
from pathlib import Path
import sys
import pandas as pd
import streamlit as st
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.charts.manufacturer_charts import bar_metric,scatter,SALES,SHARE,ND,WD,STORES,ROS,NOOS

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/"data"/"processed"
st.set_page_config(page_title="Manufacturer Comparison",layout="wide")
st.markdown("""<style>
[data-testid="stMetricValue"], [data-testid="stMetricValue"] * {font-size: .92rem !important; line-height: 1.15 !important; overflow-wrap: anywhere !important; word-break: break-word !important; white-space: normal !important;}
[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] * {font-size: .68rem !important; line-height: 1.1 !important;}
[data-testid="stMetric"] {padding: .4rem .45rem !important; min-width: 0;}
</style>""",unsafe_allow_html=True)
st.title("Manufacturer Comparison · Original Ver")
wide=pd.read_parquet(DATA/"manufacturer_dashboard_views.parquet")
insights=pd.read_json(DATA/"executive_comparison_insights.json")
states=["ALL INDIA"]+sorted(s for s in wide.State.dropna().unique() if s!="ALL INDIA"); state=st.sidebar.selectbox("State",states)
category_order=["NARTD","MANGO DRINKS","MILK DRINKS","RTD SUGAR","PDW"]
available=set(wide.loc[wide.State.eq(state),"S4CATEGORY"].unique()); cats=[c for c in category_order if c in available]; category=st.sidebar.selectbox("S4CATEGORY",cats)
top_n=st.sidebar.slider("Top N manufacturers",5,25,12); metric=st.sidebar.selectbox("Fact / Metric",[c for c in wide.columns if c not in ["State","S4CATEGORY","Manufacturer"]])
st.caption(f"{state} · {category} · Apr–Sep 2025")
d=wide[(wide.State==state)&(wide.S4CATEGORY==category)]; p=d[d.Manufacturer.eq("PARLE AGRO")]
leader=d.dropna(subset=[SALES]).nlargest(1,SALES)
cols=st.columns(6)
vals=[("Parle rank",int(d[SALES].rank(method="min",ascending=False).loc[p.index[0]]) if not p.empty and pd.notna(p.iloc[0].get(SALES)) else "NA"),("Parle Sales Value",f"{p.iloc[0].get(SALES):,.2f}" if not p.empty else "NA"),("Parle Value Share",f"{p.iloc[0].get(SHARE):.2f}%" if not p.empty and pd.notna(p.iloc[0].get(SHARE)) else "NA"),("Market leader",leader.iloc[0].Manufacturer if not leader.empty else "NA"),("Parle ND",f"{p.iloc[0].get(ND):.2f}%" if not p.empty and pd.notna(p.iloc[0].get(ND)) else "NA"),("Parle ROS",f"{p.iloc[0].get(ROS):.2f}" if not p.empty and pd.notna(p.iloc[0].get(ROS)) else "NA")]
for c,(label,value) in zip(cols,vals): c.metric(label,value)
st.plotly_chart(bar_metric(wide,state,category,SALES,"Manufacturer Sales Value Ranking",top_n),use_container_width=True)
c1,c2=st.columns(2); c1.plotly_chart(scatter(wide,state,category,ND,WD,SALES,"ND vs WD",top_n),use_container_width=True); c2.plotly_chart(scatter(wide,state,category,ND,ROS,SALES,"Distribution vs Productivity",top_n),use_container_width=True)
c3,c4=st.columns(2); c3.plotly_chart(bar_metric(wide,state,category,STORES,"Store Coverage",top_n),use_container_width=True); c4.plotly_chart(bar_metric(wide,state,category,ROS,"Rate of Sale",top_n),use_container_width=True)
match=insights[(insights.State==state)&(insights.S4CATEGORY==category)]
st.subheader("Executive insight")
if not match.empty: insight=match.iloc[0].Insight
elif p.empty or leader.empty: insight="Insufficient evidence to determine the primary performance driver."
else:
    pv=float(p.iloc[0][SALES]); lv=float(leader.iloc[0][SALES]); rank=int(d[SALES].rank(method="min",ascending=False).loc[p.index[0]]); gap=lv-pv
    insight=f"In {state} · {category}, Parle Agro ranks {rank} by Sales Value at {pv:,.2f}. {leader.iloc[0].Manufacturer} leads at {lv:,.2f}, a gap of {gap:,.2f}. Combined views use the documented aggregation rules shown below."
st.info(insight)
if state=="ALL INDIA" or category in ["PDW","NARTD"]: st.caption("Combined-view rule: additive facts are summed; ratios/rates use Sales Value-weighted averages; store coverage uses MAX across categories and SUM across states. PDW = Packaged Plain Water + RTD Mixers. NARTD = Mango + Milk + RTD Sugar + PDW.")
table=d.sort_values(SALES,ascending=False) if SALES in d else d
st.dataframe(table.head(top_n),use_container_width=True); st.download_button("Download selected comparison as CSV",table.to_csv(index=False),"manufacturer_comparison.csv","text/csv")
