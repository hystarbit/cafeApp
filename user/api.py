from bson.objectid import ObjectId
from fastapi import APIRouter, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from pymongo import ReturnDocument

from database import client
from user.schemas import User, Order

db = client.config
router = APIRouter(prefix="/cafeapp")

@router.post("/login")
async def login(
    request: User
) -> User|None:
    collection = db["users"]
    query = {"user_name": request.user_name, "password": request.password}
    doc = collection.find(query)

    if doc is not None:
        return request

    return None

@router.post(
    "/user",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    request: User,
    response: Response
) -> User|None:
    collection = db["users"]
    if len(request.user_name) >= 6 and len(request.user_name) <= 12:
        if len(request.password) >= 8 and len(request.password) <= 20:
            if "@" in request.email:
                if request.ac_star == request.now_star + request.free_drink * 10 :
                    new_article = await collection.insert_one(jsonable_encoder(request))
                    created_article = await collection.find_one({"_id": new_article.inserted_id})

                    created_article["id"] = str(created_article["_id"])

                    return created_article
    
    response.status_code = status.HTTP_400_BAD_REQUEST
    return None

@router.get("/user")
async def all_users(
    limit: int = 100,
    category: str | None = None,
) -> dict[str, list[User]]:
    collection = db["users"]

    if category is not None:
        cursor = collection.find({"category": category})
    else:
        cursor = collection.find()
    documents = []
    for user in await cursor.to_list(length=limit):
        user["id"] = str(user["_id"])
        documents.append(user)

    return {"data": documents}

@router.get("/user/{id}")
async def user(id: str) -> User:
    collection = db["users"]
    user = await collection.find_one({"_id": ObjectId(id)})

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user is found by provided id: {id}",
        )
    user["id"] = str(user["_id"])
    return user

@router.delete("/user/{id}")
async def destroy_user(
    id: str,
):
    collection = db["users"]
    delete_result = await collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user is found by provided id: {id}",
        )

    return {"msg": f"An user of id {id} is deleted."}

@router.put("/user/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_user(id: str, request: dict, response: Response) -> User|None:
    collection = db["users"]
    user = await collection.find_one({"_id": ObjectId(id)})

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user is found by provided id: {id}",
        )
    if len(request.user_name) >= 6 and len(request.user_name) <= 12:
        if len(request.password) >= 8 and len(request.password) <= 20:
            if "@" in request.email:
                if request.ac_star == request.now_star + request.free_drink * 10 :
                    updated = await collection.find_one_and_update(
                        {"_id": user["_id"]}, {"$set": request}, return_document=ReturnDocument.AFTER
                        )
                    updated["id"] = str(updated["_id"])
                    return updated
    response.status_code = status.HTTP_400_BAD_REQUEST
    return None


@router.post(
    "/order",
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    id: str,
    request: Order
) -> Order:
    collection = db["orders"]
    new_article = await collection.insert_one(jsonable_encoder(request))
    created_article = await collection.find_one({"_id": new_article.inserted_id})

    created_article["id"] = str(created_article["_id"])

    collection = db["users"]
    user = await collection.find_one({"_id": ObjectId(id)})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user is found by provided id: {id}",
        )
    user["id"] = str(user["_id"])

    updated = await collection.find_one_and_update(
            {"_id": user["_id"]}, {"$set": {"order_list": request}}, return_document=ReturnDocument.AFTER
    )
    updated["id"] = str(updated["_id"])
    

    return created_article

@router.get("/order")
async def all_orders(
    limit: int = 100,
    category: str | None = None,
) -> dict[str, list[Order]]:
    collection = db["orders"]

    if category is not None:
        cursor = collection.find({"category": category})
    else:
        cursor = collection.find()
    documents = []
    for order in await cursor.to_list(length=limit):
        order["id"] = str(order["_id"])
        documents.append(order)

    return {"data": documents}

@router.get("/order/{id}")
async def order(id: str) -> Order:
    collection = db["orders"]
    order = await collection.find_one({"_id": ObjectId(id)})

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No order is found by provided id: {id}",
        )
    order["id"] = str(order["_id"])
    return order

@router.delete("/order/{id}")
async def destroy_order(
    id: str,
):
    collection = db["orders"]
    delete_result = await collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No order is found by provided id: {id}",
        )

    return {"msg": f"An order of id {id} is deleted."}

@router.put("/order/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_order(id: str, request: dict) -> Order:
    collection = db["orders"]
    order = await collection.find_one({"_id": ObjectId(id)})

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No order is found by provided id: {id}",
        )

    updated = await collection.find_one_and_update(
        {"_id": order["_id"]}, {"$set": request}, return_document=ReturnDocument.AFTER
    )
    updated["id"] = str(updated["_id"])

    return updated