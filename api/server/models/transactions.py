from typing import Optional
from pydantic import BaseModel, Field


class TransactionSchema(BaseModel):
    description: str = Field(...)
    ammount: float = Field(...)
    target_account: str = Field(...)
    source_account: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "description": "New TV",
                "ammount": 2000.00,
                "target_account": "Boursorama",
                "source_account": None,
            }
        }


class UpdateTransactionModel(BaseModel):
    description: str = Field(...)
    ammount: float = Field(...)
    target_account: str = Field(...)
    source_account: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "description": "New TV",
                "ammount": 2000.00,
                "target_account": "Boursorama",
                "source_account": None,
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
