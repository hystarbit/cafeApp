from datetime import datetime
from pydantic import BaseModel
from menu.schemas import Menu


class Order(BaseModel):
    order_date: datetime
    menu: Menu
    count: int
    free_count: int

    class Config:
        json_schema_extra = {
            "example": {
                "order_date": "2024-01-09T19:55:30",
                "menu": {
                    "category": "coffee",
                    "menu_name": "americanoR",
                    "photo": "/",
                    "price": 4500,
                    "temperature": "cold",
                    "size": "tall"
                },
                "count": 1,
                "free_count": 0
            }
        }


class User(BaseModel):
    password: str
    user_name: str
    email: str
    phone: str
    now_star: int
    ac_star: int
    free_drink: int
    order_list: list[Order]

    class Config:
        json_schema_extra = {
            "example": {
                "user_name": "hjcafelove",
                "password": "abcde12345",
                "email": "hjlove1234@gmail.com",
                "phone": "mobile",
                "now_star": 2,
                "ac_star": 2,
                "free_drink": 0,
                "order_list": [
                    {
                        "order_date": "2024-01-09T19:55:30",
                        "menu": {
                            "category": "coffee",
                            "menu_name": "americanoR",
                            "photo": "/",
                            "price": 4500,
                            "temperature": "cold",
                            "size": "tall",
                        },
                        "count": 1,
                        "free_count": 0,
                    }
                ],
            }
        }


class Login(BaseModel):
    name: str
    password: str

    class Config:
        json_schema_extra = {"example": {"name": "ilovetea", "password": "yummy1234"}}
