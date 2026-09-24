from datetime import date
import pandas as pd
import pytest
from investment_platform.analytics import nav_returns,cumulative_performance,flow_adjusted_return,aggregate_exposures
from investment_platform.reconciliation import reconcile_nav,validate_duplicates,validate_required

def test_nav_returns_and_cumulative():
    nav=pd.Series([100,105,102,110],dtype=float)
    r=nav_returns(nav); c=cumulative_performance(r)
    assert abs(c.iloc[-1]-0.10)<1e-12

def test_flow_adjusted_return():
    assert abs(flow_adjusted_return(100,112,2)-.10)<1e-12

def test_reconciliation_and_validation():
    e=pd.DataFrame({"share_class_id":[1],"date":[date(2026,1,31)],"total_nav":[100.04]})
    f=pd.DataFrame({"share_class_id":[1],"date":[date(2026,1,31)],"total_nav":[100.00]})
    x=reconcile_nav(e,f,tolerance_bps=5)
    assert bool(x.within_tolerance.iloc[0])
    validate_required(e,["share_class_id","date","total_nav"])
    with pytest.raises(ValueError):
        validate_duplicates(pd.concat([e,e]),["share_class_id","date"])

def test_exposure_aggregation():
    d=pd.DataFrame({"date":["2026-01-31"]*2,"exposure_type":["strategy"]*2,"exposure_name":["RV"]*2,"value":[.4,.6]})
    x=aggregate_exposures(d)
    assert abs(x.value.iloc[0]-1)<1e-12
