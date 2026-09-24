import streamlit as st
import pandas as pd
from sqlalchemy import select
from investment_platform.db import make_session_factory
from investment_platform.models import Manager,Fund,ShareClass,NAVHistory,Exposure
from investment_platform.analytics import nav_returns,cumulative_performance,drawdown

st.set_page_config(page_title="Investment Analytics Platform",layout="wide")
st.title("Production-Style Investment Analytics Platform")
try:
    engine,Session=make_session_factory()
    with Session() as s:
        funds=s.execute(select(Fund.id,Fund.name,Fund.strategy)).all()
        if not funds:
            st.info("Run scripts/bootstrap_demo.py first.")
        else:
            fdf=pd.DataFrame(funds,columns=["id","fund","strategy"]); st.subheader("Portfolio overview"); st.dataframe(fdf,use_container_width=True)
            rows=s.execute(select(NAVHistory.date,NAVHistory.nav_per_share,ShareClass.name,Fund.name).join(ShareClass,NAVHistory.share_class_id==ShareClass.id).join(Fund,ShareClass.fund_id==Fund.id)).all()
            nav=pd.DataFrame(rows,columns=["date","nav_per_share","share_class","fund"])
            st.subheader("Performance")
            for fund,g in nav.groupby("fund"):
                series=g.sort_values("date").set_index("date").nav_per_share
                st.write(fund); st.line_chart((1+nav_returns(series).fillna(0)).cumprod())
            exp=s.execute(select(Exposure.date,Fund.name,Exposure.exposure_type,Exposure.exposure_name,Exposure.value).join(Fund,Exposure.fund_id==Fund.id)).all()
            if exp:
                st.subheader("Exposures"); st.dataframe(pd.DataFrame(exp,columns=["date","fund","type","name","value"]),use_container_width=True)
except Exception as exc:
    st.error("Database unavailable: "+str(exc))
