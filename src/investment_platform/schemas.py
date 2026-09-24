from datetime import date
from pydantic import BaseModel,Field,field_validator

class NAVInput(BaseModel):
    share_class_id:int
    date:date
    nav_per_share:float=Field(gt=0)
    total_nav:float=Field(gt=0)
    source:str="estimated"

class FlowInput(BaseModel):
    share_class_id:int
    date:date
    amount:float
    flow_type:str

    @field_validator("flow_type")
    @classmethod
    def valid_type(cls,v):
        if v not in {"subscription","redemption","distribution"}:
            raise ValueError("invalid flow_type")
        return v

class PositionInput(BaseModel):
    fund_id:int
    date:date
    security:str
    quantity:float
    price:float=Field(gt=0)
    asset_class:str
