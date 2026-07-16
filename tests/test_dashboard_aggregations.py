import pandas as pd
from src.metrics.dashboard_aggregations import prepare_dashboard_views

def sample():
    return pd.DataFrame([{"State":"A","S4CATEGORY":"PACKAGED PLAIN WATER","Manufacturer":"M","Sales Value (000)":100,"Numeric Distribution Handling (C)":10,"Number of Stores Retailing (C)":50},{"State":"A","S4CATEGORY":"RTD MIXERS","Manufacturer":"M","Sales Value (000)":300,"Numeric Distribution Handling (C)":30,"Number of Stores Retailing (C)":40},{"State":"B","S4CATEGORY":"PACKAGED PLAIN WATER","Manufacturer":"M","Sales Value (000)":200,"Numeric Distribution Handling (C)":20,"Number of Stores Retailing (C)":60},{"State":"A","S4CATEGORY":"MANGO DRINKS","Manufacturer":"M","Sales Value (000)":600,"Numeric Distribution Handling (C)":50,"Number of Stores Retailing (C)":70}])
def test_pdw_combination():
    d=prepare_dashboard_views(sample()); r=d[(d.State=="A")&(d.S4CATEGORY=="PDW")].iloc[0]; assert r["Sales Value (000)"]==400 and r["Numeric Distribution Handling (C)"]==25 and r["Number of Stores Retailing (C)"]==50
def test_nartd_combination():
    d=prepare_dashboard_views(sample()); r=d[(d.State=="A")&(d.S4CATEGORY=="NARTD")].iloc[0]; assert r["Sales Value (000)"]==1000 and r["Number of Stores Retailing (C)"]==70
def test_all_india():
    d=prepare_dashboard_views(sample()); r=d[(d.State=="ALL INDIA")&(d.S4CATEGORY=="PDW")].iloc[0]; assert r["Sales Value (000)"]==600 and r["Number of Stores Retailing (C)"]==110
