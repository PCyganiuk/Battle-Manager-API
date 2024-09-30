from fastapi import FastAPI
from routes.users import users_router
from routes.entry import entry_router

app = FastAPI()

app.include_router(entry_router)
app.include_router(users_router)
