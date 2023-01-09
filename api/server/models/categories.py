from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    name: str = Field(...)

    class Config:
        schema_extra = {"example": {"name": "Energie"}}


class UpdateCategoryModel(BaseModel):
    name: str = Field(...)

    class Config:
        schema_extra = {"example": {"name": "Abonnement"}}


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
