from __future__ import annotations
import logging
import pandas as pd
from .schemas import NAVInput,FlowInput,PositionInput
from .repository import Repository

log=logging.getLogger(__name__)

class InvestmentAnalyticsService:
    def __init__(self,session):
        self.session=session; self.repo=Repository(session)

    def ingest_nav(self,payload:dict):
        x=NAVInput.model_validate(payload)
        self.repo.add_nav(x.model_dump())
        log.info("ingested NAV share_class=%s date=%s",x.share_class_id,x.date)

    def ingest_flow(self,payload:dict):
        x=FlowInput.model_validate(payload)
        self.repo.add_flow(x.model_dump())

    def ingest_position(self,payload:dict):
        x=PositionInput.model_validate(payload)
        self.repo.add_position(x.model_dump())

    def nav_frame(self,share_class_id):
        rows=self.repo.nav_history(share_class_id)
        return pd.DataFrame([{"date":x.date,"nav_per_share":x.nav_per_share,"total_nav":x.total_nav,"source":x.source} for x in rows]).set_index("date")
