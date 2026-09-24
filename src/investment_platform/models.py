from __future__ import annotations
from datetime import date
from sqlalchemy import String,Float,Date,ForeignKey,UniqueConstraint,Integer
from sqlalchemy.orm import Mapped,mapped_column,relationship
from .db import Base

class Manager(Base):
    __tablename__="managers"
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(200),unique=True)
    funds:Mapped[list["Fund"]]=relationship(back_populates="manager")

class Fund(Base):
    __tablename__="funds"
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(200),unique=True)
    manager_id:Mapped[int]=mapped_column(ForeignKey("managers.id"))
    strategy:Mapped[str]=mapped_column(String(100))
    manager:Mapped["Manager"]=relationship(back_populates="funds")
    share_classes:Mapped[list["ShareClass"]]=relationship(back_populates="fund")

class ShareClass(Base):
    __tablename__="share_classes"
    id:Mapped[int]=mapped_column(primary_key=True)
    fund_id:Mapped[int]=mapped_column(ForeignKey("funds.id"))
    name:Mapped[str]=mapped_column(String(100))
    currency:Mapped[str]=mapped_column(String(10),default="USD")
    units:Mapped[float]=mapped_column(Float)
    fund:Mapped["Fund"]=relationship(back_populates="share_classes")
    __table_args__=(UniqueConstraint("fund_id","name"),)

class NAVHistory(Base):
    __tablename__="nav_history"
    id:Mapped[int]=mapped_column(primary_key=True)
    share_class_id:Mapped[int]=mapped_column(ForeignKey("share_classes.id"))
    date:Mapped[date]=mapped_column(Date)
    nav_per_share:Mapped[float]=mapped_column(Float)
    total_nav:Mapped[float]=mapped_column(Float)
    source:Mapped[str]=mapped_column(String(50),default="estimated")
    __table_args__=(UniqueConstraint("share_class_id","date"),)

class Flow(Base):
    __tablename__="flows"
    id:Mapped[int]=mapped_column(primary_key=True)
    share_class_id:Mapped[int]=mapped_column(ForeignKey("share_classes.id"))
    date:Mapped[date]=mapped_column(Date)
    amount:Mapped[float]=mapped_column(Float)
    flow_type:Mapped[str]=mapped_column(String(30))

class Position(Base):
    __tablename__="positions"
    id:Mapped[int]=mapped_column(primary_key=True)
    fund_id:Mapped[int]=mapped_column(ForeignKey("funds.id"))
    date:Mapped[date]=mapped_column(Date)
    security:Mapped[str]=mapped_column(String(100))
    quantity:Mapped[float]=mapped_column(Float)
    price:Mapped[float]=mapped_column(Float)
    market_value:Mapped[float]=mapped_column(Float)
    asset_class:Mapped[str]=mapped_column(String(50))

class StrategyAssignment(Base):
    __tablename__="strategy_assignments"
    id:Mapped[int]=mapped_column(primary_key=True)
    fund_id:Mapped[int]=mapped_column(ForeignKey("funds.id"))
    start_date:Mapped[date]=mapped_column(Date)
    end_date:Mapped[date|None]=mapped_column(Date,nullable=True)
    strategy:Mapped[str]=mapped_column(String(100))

class Exposure(Base):
    __tablename__="exposures"
    id:Mapped[int]=mapped_column(primary_key=True)
    fund_id:Mapped[int]=mapped_column(ForeignKey("funds.id"))
    date:Mapped[date]=mapped_column(Date)
    exposure_type:Mapped[str]=mapped_column(String(50))
    exposure_name:Mapped[str]=mapped_column(String(100))
    value:Mapped[float]=mapped_column(Float)
