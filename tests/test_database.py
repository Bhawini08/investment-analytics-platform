from datetime import date
import pytest
from sqlalchemy.exc import IntegrityError
from investment_platform.db import Base,make_session_factory
from investment_platform.models import Manager,Fund,ShareClass
from investment_platform.service import InvestmentAnalyticsService

def setup_db():
    engine,Session=make_session_factory("sqlite:///:memory:"); Base.metadata.create_all(engine); return Session

def test_database_ingestion_and_duplicate_guard():
    Session=setup_db()
    with Session.begin() as s:
        m=Manager(name="M"); s.add(m); s.flush(); f=Fund(name="F",manager_id=m.id,strategy="Macro"); s.add(f); s.flush()
        sc=ShareClass(fund_id=f.id,name="A",currency="USD",units=10); s.add(sc); s.flush()
        svc=InvestmentAnalyticsService(s)
        payload={"share_class_id":sc.id,"date":date(2026,1,31),"nav_per_share":100,"total_nav":1000,"source":"final"}
        svc.ingest_nav(payload)
    with Session() as s:
        svc=InvestmentAnalyticsService(s); frame=svc.nav_frame(1); assert len(frame)==1

def test_schema_rejects_negative_nav():
    Session=setup_db()
    with Session.begin() as s:
        svc=InvestmentAnalyticsService(s)
        with pytest.raises(Exception):
            svc.ingest_nav({"share_class_id":1,"date":date(2026,1,31),"nav_per_share":-1,"total_nav":100,"source":"final"})
