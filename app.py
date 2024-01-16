"Main app"


from fastapi import FastAPI

from menu.api import router as router_menu
from user.api import router as router_user

app = FastAPI()

app.include_router(router_menu)
app.include_router(router_user)