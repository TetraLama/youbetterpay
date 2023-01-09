from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, datetime, time, timedelta


class TransactionSchema(BaseModel):
    description: str = Field(...)
    ammount: str = Field(...)
    type: str = Field(...)
    category: str = Field(...)
    target_account: str = Field(...)
    dest_account: Optional[str]
    date: Optional[date]
    ammount_is_calculated: Optional[bool]
    is_reccurent: Optional[bool]
    frequency_every_number: Optional[int]
    freccurency_every_unit: Optional[str]
    date_end_reccurency: Optional[date]

    class Config:
        schema_extra = {
            "example": {
                "description": "New TV",
                "ammount": "2000.00",
                "type": "ObjectID MongoDB(ex: 5fec2c0b348df9f22156cc07)",
                "category": "ObjectID MongoDB(ex: 5fec2c0b348df9f22156cc07)",
                "target_account": "ObjectID MongoDB(ex: 5fec2c0b348df9f22156cc07)",
                "dest_account": None,
                "date": "2022-12-24",
                "ammount_is_calculated": False,
                "is_reccurent": False,
                "frequency_every_number": None,
                "freccurency_every_unit": None,
                "date_end_reccurency": None,
            }
        }


class UpdateTransactionModel(BaseModel):
    description: str = Field(...)
    ammount: str = Field(...)
    type: str = Field(...)
    category: str = Field(...)
    target_account: str = Field(...)
    dest_account: Optional[str]
    date: Optional[date]
    ammount_is_calculated: Optional[bool]
    is_reccurent: Optional[bool]
    frequency_every_number: Optional[int]
    freccurency_every_unit: Optional[str]
    date_end_reccurency: Optional[date]

    class Config:
        schema_extra = {
            "example": {
                "description": "New TV",
                "ammount": "calculated",
                "type": "ObjectID MongoDB(ex: 5fec2c0b348df9f22156cc07)",
                "target_account": "ObjectID MongoDB(ex: 5fec2c0b348df9f22156cc07)",
                "dest_account": None,
                "date": "2022-12-24",
                "ammount_is_calculated": False,
                "is_reccurent": False,
                "frequency_every_number": None,
                "freccurency_every_unit": None,
                "date_end_reccurency": None,
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
