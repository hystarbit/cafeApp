from bson.objectid import ObjectId
from fastapi import APIRouter, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from pymongo import ReturnDocument

from database import client
from menu.schemas import Menu

db = client.config
router = APIRouter(prefix="/cafeapp")

@router.post(
    "/menu",
    status_code=status.HTTP_201_CREATED,
)
async def create_menu(
    request: Menu,
    response: Response
) -> Menu|None:
    collection = db["menus"]
    if request.temperature in ["hot", "cold"]:
        if request.size in ["tall", "grande", "venti"]:

            new_article = await collection.insert_one(jsonable_encoder(request))
            created_article = await collection.find_one({"_id": new_article.inserted_id})

            created_article["id"] = str(created_article["_id"])

            return created_article
    response.status_code = status.HTTP_400_BAD_REQUEST
    return None

@router.get("/menu")
async def all_menus(
    limit: int = 100,
    category: str | None = None,
) -> dict[str, list[Menu]]:
    collection = db["menus"]

    if category is not None:
        cursor = collection.find({"category": category})
    else:
        cursor = collection.find()
    documents = []
    for menu in await cursor.to_list(length=limit):
        menu["id"] = str(menu["_id"])
        documents.append(menu)

    return {"data": documents}

@router.get("/menu/{id}")
async def menu(id: str) -> Menu:
    collection = db["menus"]
    menu = await collection.find_one({"_id": ObjectId(id)})

    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No menu is found by provided id: {id}",
        )
    menu["id"] = str(menu["_id"])
    return menu

@router.delete("/menu/{id}")
async def destroy_menu(
    id: str,
):
    collection = db["menus"]
    delete_result = await collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No menu is found by provided id: {id}",
        )

    return {"msg": f"A menu of id {id} is deleted."}

@router.put("/menu/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_menu(id: str, request: dict, response: Response) -> Menu|None:
    collection = db["menus"]

    menu = await collection.find_one({"_id": ObjectId(id)})

    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No menu is found by provided id: {id}",
        )
    if request.temperature in ["hot", "cold"]:
        if request.size == ["tall", "grande", "venti"]:
            updated = await collection.find_one_and_update(
                {"_id": menu["_id"]}, {"$set": request}, return_document=ReturnDocument.AFTER
                )
            updated["id"] = str(updated["_id"])

            return updated
    response.status_code = status.HTTP_400_BAD_REQUEST
    return None

