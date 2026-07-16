"""Reusable Plotly manufacturer benchmarking charts with visible data labels."""

from __future__ import annotations
from pathlib import Path
import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

PARLE="PARLE AGRO"; PARLE_COLOR="#E31E24"; LEADER_COLOR="#F5A623"; OTHER="#AAB4C3"
SALES="Sales Value (000)"; SHARE="Share of Sales Value - Product"; ND="Numeric Distribution Handling (C)"; WD="Wghtd Dist Handling (C) - CATEGORY"; STORES="Number of Stores Retailing (C)"; ROS="Unwghtd ROS (VOL UNIT CASES) Handling (C)"; PRICE="Price per Sales Unit"; NOOS="Numeric Out of Stock (C)"; WOOS="Wghtd Dist Out of Stock"


def subset(wide,state,category): return wide[(wide.State==state)&(wide.S4CATEGORY==category)].copy()
def colors(df,metric):
    leader=df.loc[df[metric].idxmax(),"Manufacturer"] if not df.empty else ""
    return [PARLE_COLOR if m==PARLE else LEADER_COLOR if m==leader else OTHER for m in df.Manufacturer]
def bar_metric(wide,state,category,metric,title,top_n=15):
    d=subset(wide,state,category).dropna(subset=[metric]).nlargest(top_n,metric).sort_values(metric)
    fig=go.Figure(go.Bar(x=d[metric],y=d.Manufacturer,orientation="h",marker_color=colors(d,metric),text=[f"{v:,.2f}" for v in d[metric]],textposition="auto",insidetextanchor="end",customdata=d.Manufacturer,hovertemplate="%{customdata}<br>Value: %{x:,.3f}<extra></extra>"))
    fig.update_layout(title=f"{title}<br><sup>{state} · {category}</sup>",xaxis_title=metric,yaxis_title="",margin=dict(l=220,r=70,t=90,b=60)); return fig
def scatter(wide,state,category,x,y,size,title,top_n=12):
    cols=["Manufacturer",x,y,size]; d=subset(wide,state,category).dropna(subset=[x,y,size]).nlargest(top_n,size)
    d["Role"]=d.Manufacturer.map(lambda m:"Parle Agro" if m==PARLE else "Other manufacturer")
    label_names=set(d.nlargest(4,size).Manufacturer.tolist()+[PARLE])
    d["Chart Label"]=d.apply(lambda r:f"{r.Manufacturer}<br>{r[x]:.1f}, {r[y]:.1f}" if r.Manufacturer in label_names else "",axis=1)
    fig=px.scatter(d,x=x,y=y,size=size,color="Role",text="Chart Label",color_discrete_map={"Parle Agro":PARLE_COLOR,"Other manufacturer":OTHER},hover_name="Manufacturer",hover_data={x:":.2f",y:":.2f",size:":,.2f"})
    fig.update_traces(textposition="top center",textfont_size=9)
    fig.update_layout(title=f"{title}<br><sup>{state} · {category}; labels show X, Y values</sup>",margin=dict(l=80,r=80,t=105,b=75))
    return fig


def build_suite(wide:pd.DataFrame,insights:pd.DataFrame,state:str,category:str):
    figs=[]
    figs.append(("01_sales_value_ranking","Manufacturer Sales Value Ranking",bar_metric(wide,state,category,SALES,"Manufacturer Sales Value Ranking")))
    figs.append(("02_value_share","Manufacturer Value Share Comparison",bar_metric(wide,state,category,SHARE,"Manufacturer Value Share Comparison")))
    figs.append(("03_nd_vs_wd","Numeric Distribution vs Weighted Distribution",scatter(wide,state,category,ND,WD,SALES,"Numeric Distribution vs Weighted Distribution")))
    figs.append(("04_distribution_productivity","Distribution vs Productivity Matrix",scatter(wide,state,category,ND,ROS,SALES,"Distribution vs Productivity Matrix")))
    figs.append(("05_sales_vs_share","Sales Value vs Market Share",scatter(wide,state,category,SALES,SHARE,SALES,"Sales Value vs Market Share")))
    figs.append(("06_store_coverage","Store Coverage Comparison",bar_metric(wide,state,category,STORES,"Number of Stores Retailing")))
    figs.append(("07_rate_of_sale","Rate of Sale Comparison",bar_metric(wide,state,category,ROS,"Rate of Sale Comparison")))
    figs.append(("08_price_positioning","Price Positioning",bar_metric(wide,state,category,PRICE,"Price per Sales Unit")))
    d=subset(wide,state,category).dropna(subset=[NOOS],how="all").copy(); d=d.nlargest(15,SALES) if SALES in d else d.head(15)
    fig=go.Figure();
    if NOOS in d: fig.add_bar(x=d.Manufacturer,y=d[NOOS],name="Numeric OOS",text=d[NOOS].map(lambda v:f"{v:.1f}"),textposition="outside")
    if WOOS in d: fig.add_bar(x=d.Manufacturer,y=d[WOOS],name="Weighted OOS",text=d[WOOS].map(lambda v:f"{v:.1f}" if pd.notna(v) else ""),textposition="outside")
    fig.update_layout(barmode="group",title=f"Out-of-Stock Comparison<br><sup>{state} · {category}</sup>",xaxis_tickangle=-35)
    figs.append(("09_out_of_stock","Out-of-Stock Comparison",fig))
    metrics=[m for m in [SALES,SHARE,ND,WD,STORES,ROS] if m in wide]
    h=subset(wide,state,category).dropna(subset=[SALES]).nlargest(12,SALES).set_index("Manufacturer")[metrics]
    norm=h.rank(pct=True)*100
    fig=px.imshow(norm,text_auto=".0f",aspect="auto",color_continuous_scale="Blues",labels={"color":"Percentile score"}); fig.update_layout(title=f"Manufacturer Performance Heatmap<br><sup>{state} · {category}; percentile normalisation within selection</sup>")
    figs.append(("10_performance_heatmap","Manufacturer Performance Heatmap",fig))
    opp=insights.pivot(index="State",columns="S4CATEGORY",values="Gap")
    fig=px.imshow(opp,text_auto=".3s",aspect="auto",color_continuous_scale="Reds",labels={"color":"Sales gap"}); fig.update_layout(title="Parle Opportunity Heatmap: Sales Value Gap to Leader")
    figs.append(("11_opportunity_heatmap","State × S4CATEGORY Opportunity Heatmap",fig))
    rank_matrix=insights.pivot(index="State",columns="S4CATEGORY",values="Parle_Rank")
    fig=px.imshow(rank_matrix,text_auto=".0f",aspect="auto",color_continuous_scale="RdYlGn_r",labels={"color":"Parle rank"})
    fig.update_layout(title="Parle Rank Across States<br><sup>Rank 1 is best; blank means insufficient sales data</sup>",xaxis_title="S4CATEGORY",yaxis_title="State",margin=dict(l=125,r=60,t=90,b=70))
    figs.append(("12_parle_rank_states","Parle Rank Across States",fig))
    gap=insights.sort_values("Gap",ascending=True); gap["Combination"]=gap.State+" · "+gap.S4CATEGORY
    fig=go.Figure(); fig.add_bar(y=gap.Combination,x=gap.Parle_Value,orientation="h",name="Parle",marker_color=PARLE_COLOR,text=gap.Parle_Value.map(lambda v:f"{v:,.0f}"),textposition="inside"); fig.add_bar(y=gap.Combination,x=gap.Leader_Value,orientation="h",name="Leader",marker_color=LEADER_COLOR,text=gap.Leader_Value.map(lambda v:f"{v:,.0f}"),textposition="outside"); fig.update_layout(barmode="group",height=max(900,len(gap)*28),title="Parle vs Market Leader: Sales Value Gap",legend=dict(orientation="h",x=.5,xanchor="center",y=-.06,yanchor="top"),margin=dict(l=250,r=110,t=85,b=110))
    figs.append(("13_leader_gap","Leader Gap Chart",fig))
    for _,_,fig in figs:
        fig.update_layout(template="plotly_white",font=dict(family="Arial",size=12),hoverlabel=dict(namelength=-1),margin_pad=8)
    return figs


def save_suite(figs,out:Path,write_images=False):
    out.mkdir(parents=True,exist_ok=True); items=[]
    for slug,title,fig in figs:
        html_name=slug+".html"; png_name=slug+".png"
        fig.write_html(out/html_name,include_plotlyjs="directory",full_html=True,config={"responsive":True,"displaylogo":False})
        if write_images: fig.write_image(out/png_name,width=1400,height=800,scale=1)
        items.append((html_name,png_name,title))
    links="".join(f'<li><a href="{html.escape(h)}">{html.escape(t)}</a></li>' for h,_,t in items)
    (out/"index.html").write_text(f'<!doctype html><meta charset="utf-8"><title>Manufacturer Benchmarking</title><style>body{{font-family:Arial;max-width:950px;margin:40px auto}}li{{margin:14px}}</style><h1>Original Ver Manufacturer Benchmarking</h1><ol>{links}</ol>',encoding="utf-8")
    return items
