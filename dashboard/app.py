import streamlit as st
import pandas as pd
from sqlalchemy import select
from investment_platform.db import make_session_factory
from investment_platform.models import Manager,Fund,ShareClass,NAVHistory,Exposure
from investment_platform.analytics import nav_returns,annualized_metrics

st.set_page_config(page_title="Investment Analytics Platform",layout="wide")
st.title("Production-Style Investment Analytics Platform")

page=st.sidebar.radio("Page",["Portfolio Overview","Performance","Manager Analysis","Attribution","Exposures","Risk"])

try:
    engine,Session=make_session_factory()
    with Session() as s:
        fund_rows=s.execute(
            select(Fund.id,Fund.name,Fund.strategy,Manager.name)
            .join(Manager,Fund.manager_id==Manager.id)
        ).all()
        if not fund_rows:
            st.info("Run scripts/bootstrap_demo.py first.")
            st.stop()

        funds=pd.DataFrame(fund_rows,columns=["fund_id","fund","strategy","manager"])
        nav_rows=s.execute(
            select(NAVHistory.date,NAVHistory.nav_per_share,NAVHistory.total_nav,
                   ShareClass.name,Fund.id,Fund.name,Manager.name)
            .join(ShareClass,NAVHistory.share_class_id==ShareClass.id)
            .join(Fund,ShareClass.fund_id==Fund.id)
            .join(Manager,Fund.manager_id==Manager.id)
        ).all()
        nav=pd.DataFrame(nav_rows,columns=["date","nav_per_share","total_nav","share_class","fund_id","fund","manager"])
        exp_rows=s.execute(
            select(Exposure.date,Fund.name,Exposure.exposure_type,Exposure.exposure_name,Exposure.value)
            .join(Fund,Exposure.fund_id==Fund.id)
        ).all()
        exposures=pd.DataFrame(exp_rows,columns=["date","fund","type","name","value"]) if exp_rows else pd.DataFrame()

        if page=="Portfolio Overview":
            st.subheader("Portfolio overview")
            latest=nav.sort_values("date").groupby("fund",as_index=False).tail(1)
            overview=funds.merge(latest[["fund","date","total_nav","nav_per_share"]],on="fund",how="left")
            c1,c2,c3=st.columns(3)
            c1.metric("Funds",len(overview))
            c2.metric("Managers",overview.manager.nunique())
            c3.metric("Latest aggregate NAV","$"+format(overview.total_nav.sum(),",.0f"))
            st.dataframe(overview,use_container_width=True)

        elif page=="Performance":
            st.subheader("Performance")
            for fund,g in nav.groupby("fund"):
                series=g.sort_values("date").set_index("date").nav_per_share
                r=nav_returns(series)
                st.write("**"+fund+"**")
                st.line_chart((1+r.fillna(0)).cumprod())
                st.json(annualized_metrics(r))

        elif page=="Manager Analysis":
            st.subheader("Manager analysis")
            latest=nav.sort_values("date").groupby("fund",as_index=False).tail(1)
            manager=latest.groupby("manager",as_index=False).agg(
                total_nav=("total_nav","sum"),
                funds=("fund","nunique")
            )
            st.dataframe(manager,use_container_width=True)
            st.bar_chart(manager.set_index("manager")[["total_nav"]])

        elif page=="Attribution":
            st.subheader("Latest-period contribution attribution")
            rows=[]
            latest_total=0.0
            temp=[]
            for fund,g in nav.groupby("fund"):
                g=g.sort_values("date")
                if len(g)<2:
                    continue
                ending=float(g.total_nav.iloc[-1])
                ret=float(g.nav_per_share.iloc[-1]/g.nav_per_share.iloc[-2]-1)
                temp.append((fund,ending,ret))
                latest_total+=ending
            for fund,ending,ret in temp:
                weight=ending/latest_total if latest_total else 0.0
                rows.append({"fund":fund,"weight":weight,"period_return":ret,"contribution":weight*ret})
            attr=pd.DataFrame(rows)
            st.dataframe(attr,use_container_width=True)
            if not attr.empty:
                st.bar_chart(attr.set_index("fund")[["contribution"]])

        elif page=="Exposures":
            st.subheader("Exposures")
            if exposures.empty:
                st.info("No exposure records available.")
            else:
                latest_date=exposures.date.max()
                latest=exposures[exposures.date==latest_date]
                st.caption("Latest exposure date: "+str(latest_date))
                st.dataframe(latest,use_container_width=True)
                pivot=latest.pivot_table(index="name",columns="fund",values="value",aggfunc="sum",fill_value=0)
                st.bar_chart(pivot)

        elif page=="Risk":
            st.subheader("Fund risk")
            risk=[]
            for fund,g in nav.groupby("fund"):
                series=g.sort_values("date").set_index("date").nav_per_share
                risk.append({"fund":fund,**annualized_metrics(nav_returns(series))})
            risk=pd.DataFrame(risk)
            st.dataframe(risk,use_container_width=True)
            if not risk.empty:
                st.bar_chart(risk.set_index("fund")[["annualized_volatility","max_drawdown"]])

except Exception as exc:
    st.error("Database unavailable: "+str(exc))
