from datetime import date
import logging
import numpy as np
from investment_platform.db import Base,make_session_factory
from investment_platform.models import Manager,Fund,ShareClass,Exposure
from investment_platform.service import InvestmentAnalyticsService

logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(name)s %(message)s")
engine,Session=make_session_factory(); Base.metadata.drop_all(engine); Base.metadata.create_all(engine)
rng=np.random.default_rng(5)
with Session.begin() as s:
    m1=Manager(name="Northstar Capital"); m2=Manager(name="Meridian Partners"); s.add_all([m1,m2]); s.flush()
    f1=Fund(name="Northstar Digital Opportunities",manager_id=m1.id,strategy="Relative Value")
    f2=Fund(name="Meridian Multi-Strategy",manager_id=m2.id,strategy="Multi-Strategy"); s.add_all([f1,f2]); s.flush()
    sc1=ShareClass(fund_id=f1.id,name="Class A",currency="USD",units=100000); sc2=ShareClass(fund_id=f2.id,name="Class I",currency="USD",units=150000)
    s.add_all([sc1,sc2]); s.flush(); svc=InvestmentAnalyticsService(s)
    navs={sc1.id:100.0,sc2.id:100.0}
    for month in range(24):
        d=date(2024+month//12,month%12+1,28)
        for sc in [sc1,sc2]:
            navs[sc.id]*=(1+rng.normal(.008,.035))
            svc.ingest_nav({"share_class_id":sc.id,"date":d,"nav_per_share":navs[sc.id],"total_nav":navs[sc.id]*sc.units,"source":"final"})
        for fund in [f1,f2]:
            for typ,name,val in [("strategy",fund.strategy,1.0),("asset_class","Digital Assets" if fund is f1 else "Multi-Asset",1.0)]:
                s.add(Exposure(fund_id=fund.id,date=d,exposure_type=typ,exposure_name=name,value=val))
print("Demo database created.")
