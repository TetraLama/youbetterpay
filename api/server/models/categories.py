from typing import Optional
from pydantic import BaseModel, Field

class CategorySchema(BaseModel):
    name: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Internal Transfert"
            }
        }


class UpdateCategoryModel(BaseModel):
    description: str = Field(...)
    ammount: float = Field(...)
    target_account: str = Field(...)
    source_account: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Internal Transfert"
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