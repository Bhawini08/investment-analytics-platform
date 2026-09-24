from __future__ import annotations
import numpy as np
import pandas as pd

def nav_returns(nav: pd.Series) -> pd.Series:
    s=pd.Series(nav,dtype=float)
    if (s<=0).any(): raise ValueError("NAV must be positive")
    return s.pct_change()

def cumulative_performance(returns: pd.Series) -> pd.Series:
    return (1+pd.Series(returns).fillna(0)).cumprod()-1

def drawdown(returns: pd.Series) -> pd.Series:
    wealth=(1+pd.Series(returns).fillna(0)).cumprod()
    return wealth/wealth.cummax()-1

def annualized_metrics(returns: pd.Series, periods=12):
    r=pd.Series(returns).dropna()
    if len(r)==0: return {"annualized_return":np.nan,"annualized_volatility":np.nan,"sharpe":np.nan,"max_drawdown":np.nan}
    ann=(1+r).prod()**(periods/len(r))-1
    vol=r.std(ddof=1)*np.sqrt(periods) if len(r)>1 else 0.0
    sharpe=(r.mean()/r.std(ddof=1)*np.sqrt(periods)) if len(r)>1 and r.std(ddof=1)>0 else np.nan
    mdd=float(drawdown(r).min())
    return {"annualized_return":float(ann),"annualized_volatility":float(vol),"sharpe":float(sharpe),"max_drawdown":mdd}

def aggregate_exposures(df: pd.DataFrame, group_cols=("date","exposure_type","exposure_name")):
    req=set(group_cols)|{"value"}
    if not req.issubset(df.columns): raise ValueError("missing exposure columns")
    return df.groupby(list(group_cols),as_index=False)["value"].sum()

def aggregate_manager_nav(df: pd.DataFrame):
    req={"date","manager","total_nav"}
    if not req.issubset(df.columns): raise ValueError("missing manager NAV columns")
    return df.groupby(["date","manager"],as_index=False)["total_nav"].sum()

def flow_adjusted_return(begin_nav,end_nav,net_flow):
    if begin_nav<=0: raise ValueError("begin_nav must be positive")
    return (end_nav-net_flow)/begin_nav-1
