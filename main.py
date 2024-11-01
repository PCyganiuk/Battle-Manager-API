from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi import FastAPI
from routes.users import users_router
from routes.entry import entry_router
from routes.games import games_router
from routes.pawns import pawns_router

app = FastAPI()

app.include_router(entry_router)
app.include_router(users_router)
app.include_router(games_router)
app.include_router(pawns_router)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173" #TODO change link to frontend when ready
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)