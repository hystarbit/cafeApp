from datetime import datetime
from pydantic import BaseModel

class Menu(BaseModel):
    category: str 
    menu_name: str
    photo: str
    price: int
    temperature: str
    size: str

    class Config:
        json_schema_extra = {
            "example": {
                "category": "coffee",
                "menu_name": "americanoR",
                "photo": "/",
                "price": 4500,
                "temperature": "cold",
                "size": "tall",
            }
        }