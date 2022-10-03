from typing import Optional
from pydantic import BaseModel, Field


class TypeSchema(BaseModel):
    name: str = Field(...)

    class Config:
        schema_extra = {"example": {"name": "Category Name"}}


class UpdateTypeModel(BaseModel):
    name: Optional[str]

    class Config:
        schema_extra = {"example": {"name": "Category Name"}}


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
