from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from api.server.database import (
    add_category,
    delete_category,
    retrieve_category,
    retrieve_categories,
    update_category,
)
from api.server.models.categories import (
    ErrorResponseModel,
    ResponseModel,
    CategorySchema,
    UpdateCategoryModel,
)

router = APIRouter()


@router.post("/", response_description="Category added into the database")
async def add_category_data(category: CategorySchema = Body(...)):
    category = jsonable_encoder(category)
    new_category = await add_category(category)
    return ResponseModel(new_category, "Category added successfully.")


@router.get("/", response_description="Categories retrieved")
async def get_categories():
    categories = await retrieve_categories()
    if categories:
        return ResponseModel(categories, "Categories data retrieved successfully")
    return ResponseModel(categories, "Empty list returned")


@router.get("/{id}", response_description="Category retrieved")
async def get_category_data(id):
    category = await retrieve_category(id)
    if category:
        return ResponseModel(category, "Category data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Category doesn't exist.")


@router.put("/{id}")
async def update_category_data(id: str, req: UpdateCategoryModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_category = await update_category(id, req)
    if updated_category:
        return ResponseModel(
            "Category with ID: {} name update is successful".format(id),
            "Category name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the category data.",
    )


@router.delete("/{id}", response_description="Category data deleted from the database")
async def delete_category_data(id: str):
    deleted_category = await delete_category(id)
    if deleted_category:
        return ResponseModel(
            f"Category with ID: {id} removed", "Category deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, f"Category with id {id} doesn't exist"
    )
