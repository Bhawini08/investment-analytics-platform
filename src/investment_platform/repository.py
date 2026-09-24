from sqlalchemy import select
from .models import NAVHistory,Flow,Position,Exposure

class Repository:
    def __init__(self,session): self.session=session

    def add_nav(self,row):
        self.session.add(NAVHistory(**row)); self.session.flush()

    def add_flow(self,row):
        self.session.add(Flow(**row)); self.session.flush()

    def add_position(self,row):
        row=dict(row); row["market_value"]=row.get("market_value",row["quantity"]*row["price"])
        self.session.add(Position(**row)); self.session.flush()

    def add_exposure(self,row):
        self.session.add(Exposure(**row)); self.session.flush()

    def nav_history(self,share_class_id):
        return list(self.session.scalars(select(NAVHistory).where(NAVHistory.share_class_id==share_class_id).order_by(NAVHistory.date)))

    def positions_for_fund(self,fund_id):
        return list(self.session.scalars(select(Position).where(Position.fund_id==fund_id).order_by(Position.date)))

    def exposures_for_fund(self,fund_id):
        return list(self.session.scalars(select(Exposure).where(Exposure.fund_id==fund_id).order_by(Exposure.date)))
