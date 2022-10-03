from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from api.server.database import (
    add_type,
    delete_type,
    retrieve_type,
    retrieve_types,
    update_type,
)
from api.server.models.types import (
    ErrorResponseModel,
    ResponseModel,
    TypeSchema,
    UpdateTypeModel,
)

router = APIRouter()


@router.post("/", response_description="type data added into the database")
async def add_type_data(type: TypeSchema = Body(...)):
    type = jsonable_encoder(type)
    new_type = await add_type(type)
    return ResponseModel(new_type, "type added successfully.")


@router.get("/", response_description="types retrieved")
async def get_types():
    types = await retrieve_types()
    if types:
        return ResponseModel(types, "types data retrieved successfully")
    return ResponseModel(types, "Empty list returned")


@router.get("/{id}", response_description="type data retrieved")
async def get_type_data(id):
    type = await retrieve_type(id)
    if type:
        return ResponseModel(type, "Student data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "type doesn't exist.")


@router.put("/{id}")
async def update_type_data(id: str, req: UpdateTypeModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_type = await update_type(id, req)
    if updated_type:
        return ResponseModel(
            "type with ID: {} name update is successful".format(id),
            "type name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the type data.",
    )


@router.delete("/{id}", response_description="type data deleted from the database")
async def delete_type_data(id: str):
    deleted_type = await delete_type(id)
    if deleted_type:
        return ResponseModel(
            "type with ID: {} removed".format(id), "type deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "type with id {0} doesn't exist".format(id)
    )
