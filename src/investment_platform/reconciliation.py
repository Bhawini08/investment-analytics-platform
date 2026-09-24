from __future__ import annotations
import pandas as pd

def reconcile_nav(estimated: pd.DataFrame,final: pd.DataFrame,tolerance_bps=5.0):
    keys=["share_class_id","date"]
    e=estimated[keys+["total_nav"]].rename(columns={"total_nav":"estimated_nav"})
    f=final[keys+["total_nav"]].rename(columns={"total_nav":"final_nav"})
    x=e.merge(f,on=keys,how="outer",indicator=True)
    x["difference"]=x["estimated_nav"]-x["final_nav"]
    x["difference_bps"]=x["difference"]/x["final_nav"]*1e4
    x["within_tolerance"]=x["difference_bps"].abs()<=tolerance_bps
    x.loc[x["_merge"]!="both","within_tolerance"]=False
    return x

def validate_duplicates(df: pd.DataFrame,keys):
    dup=df.duplicated(list(keys),keep=False)
    if dup.any():
        raise ValueError("duplicate records detected: "+str(df.loc[dup,list(keys)].to_dict("records")[:5]))
    return True

def validate_required(df: pd.DataFrame,columns):
    missing=[c for c in columns if c not in df.columns]
    if missing: raise ValueError("missing required columns: "+", ".join(missing))
    if df[list(columns)].isna().any().any(): raise ValueError("null values in required columns")
    return True
